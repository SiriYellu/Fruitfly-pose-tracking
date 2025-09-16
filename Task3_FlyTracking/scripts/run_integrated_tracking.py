#!/usr/bin/env python3
"""
Integrated Fly Tracking Pipeline for Task 3
Uses Task 2 pose estimation results for multi-object tracking
Implements ByteTrack-style tracking with pose-based association
"""

import os
import sys
import json
import numpy as np
import pandas as pd
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict
from collections import defaultdict
import argparse
from datetime import datetime
import cv2

@dataclass
class Detection:
    """Single fly detection with pose information"""
    frame_id: str
    bbox: Tuple[float, float, float, float]  # x_center, y_center, width, height (normalized)
    keypoints: List[Tuple[float, float, float]]  # (x, y, visibility) for each keypoint
    confidence: float = 1.0
    track_id: Optional[int] = None

@dataclass
class Track:
    """Track representing a single fly across multiple frames"""
    track_id: int
    detections: List[Detection]
    last_seen: int
    is_active: bool = True
    start_frame: int = 0
    
    @property
    def length(self):
        return len(self.detections)
    
    @property
    def last_detection(self):
        return self.detections[-1] if self.detections else None

class IntegratedFlyTracker:
    """Multi-object tracker for flies using pose-based association"""
    
    def __init__(self, 
                 max_disappeared: int = 15,
                 max_distance: float = 0.15,
                 pose_weight: float = 0.7,
                 bbox_weight: float = 0.3,
                 min_track_length: int = 5):
        self.max_disappeared = max_disappeared
        self.max_distance = max_distance
        self.pose_weight = pose_weight
        self.bbox_weight = bbox_weight
        self.min_track_length = min_track_length
        
        self.next_track_id = 0
        self.tracks: Dict[int, Track] = {}
        self.frame_count = 0
        
    def parse_yolo_pose_label(self, label_file: str, frame_id: str) -> List[Detection]:
        """Parse YOLO pose label file into Detection objects"""
        detections = []
        
        if not os.path.exists(label_file):
            return detections
            
        try:
            with open(label_file, 'r') as f:
                lines = f.readlines()
                
            for line in lines:
                parts = line.strip().split()
                if len(parts) < 7:  # Need at least class + bbox + 1 keypoint
                    continue
                    
                # Parse YOLO format: class x_center y_center width height kp1_x kp1_y kp1_v ...
                class_id = int(parts[0])
                x_center = float(parts[1])
                y_center = float(parts[2])
                width = float(parts[3])
                height = float(parts[4])
                
                # Parse keypoints (head, thorax, abdomen)
                keypoints = []
                for i in range(5, len(parts), 3):
                    if i + 2 < len(parts):
                        kp_x = float(parts[i])
                        kp_y = float(parts[i + 1])
                        kp_v = float(parts[i + 2])
                        keypoints.append((kp_x, kp_y, kp_v))
                
                detection = Detection(
                    frame_id=frame_id,
                    bbox=(x_center, y_center, width, height),
                    keypoints=keypoints,
                    confidence=1.0
                )
                detections.append(detection)
                
        except Exception as e:
            print(f"Error parsing {label_file}: {e}")
            
        return detections
    
    def calculate_distance(self, det1: Detection, det2: Detection) -> float:
        """Calculate weighted distance between two detections"""
        # Bounding box distance (center point)
        bbox_dist = np.sqrt(
            (det1.bbox[0] - det2.bbox[0])**2 + 
            (det1.bbox[1] - det2.bbox[1])**2
        )
        
        # Pose distance (average keypoint distance)
        pose_dist = 0.0
        if det1.keypoints and det2.keypoints:
            min_kp = min(len(det1.keypoints), len(det2.keypoints))
            for i in range(min_kp):
                kp1 = det1.keypoints[i]
                kp2 = det2.keypoints[i]
                if kp1[2] > 0.5 and kp2[2] > 0.5:  # Both keypoints visible
                    pose_dist += np.sqrt((kp1[0] - kp2[0])**2 + (kp1[1] - kp2[1])**2)
            pose_dist /= min_kp if min_kp > 0 else 1
        
        # Weighted combination
        total_dist = self.pose_weight * pose_dist + self.bbox_weight * bbox_dist
        return total_dist
    
    def associate_detections(self, detections: List[Detection]) -> List[Tuple[int, int]]:
        """Associate detections with existing tracks using Hungarian algorithm"""
        if not detections or not self.tracks:
            return []
        
        # Create cost matrix
        active_tracks = {tid: track for tid, track in self.tracks.items() if track.is_active}
        if not active_tracks:
            return []
        
        cost_matrix = np.full((len(detections), len(active_tracks)), np.inf)
        
        for i, detection in enumerate(detections):
            for j, (track_id, track) in enumerate(active_tracks.items()):
                if track.last_detection:
                    distance = self.calculate_distance(detection, track.last_detection)
                    if distance <= self.max_distance:
                        cost_matrix[i, j] = distance
        
        # Simple greedy assignment (can be replaced with Hungarian algorithm)
        assignments = []
        used_tracks = set()
        
        # Sort by cost
        indices = np.unravel_index(np.argsort(cost_matrix.ravel()), cost_matrix.shape)
        
        for i, j in zip(indices[0], indices[1]):
            if cost_matrix[i, j] < np.inf and j not in used_tracks:
                assignments.append((i, list(active_tracks.keys())[j]))
                used_tracks.add(j)
        
        return assignments
    
    def update(self, detections: List[Detection]) -> List[Track]:
        """Update tracker with new detections"""
        self.frame_count += 1
        
        # Associate detections with existing tracks
        assignments = self.associate_detections(detections)
        assigned_detections = set()
        assigned_tracks = set()
        
        # Update assigned tracks
        for det_idx, track_id in assignments:
            detection = detections[det_idx]
            detection.track_id = track_id
            
            if track_id in self.tracks:
                self.tracks[track_id].detections.append(detection)
                self.tracks[track_id].last_seen = self.frame_count
                self.tracks[track_id].is_active = True
            
            assigned_detections.add(det_idx)
            assigned_tracks.add(track_id)
        
        # Create new tracks for unassigned detections
        for i, detection in enumerate(detections):
            if i not in assigned_detections:
                track_id = self.next_track_id
                self.next_track_id += 1
                
                detection.track_id = track_id
                track = Track(
                    track_id=track_id,
                    detections=[detection],
                    last_seen=self.frame_count,
                    is_active=True,
                    start_frame=self.frame_count
                )
                self.tracks[track_id] = track
        
        # Update track states
        for track_id, track in self.tracks.items():
            if track_id not in assigned_tracks:
                if self.frame_count - track.last_seen > self.max_disappeared:
                    track.is_active = False
        
        # Return active tracks
        active_tracks = [track for track in self.tracks.values() if track.is_active]
        return active_tracks
    
    def get_all_tracks(self) -> List[Track]:
        """Get all tracks (active and inactive)"""
        return list(self.tracks.values())
    
    def get_valid_tracks(self) -> List[Track]:
        """Get tracks that meet minimum length requirement"""
        return [track for track in self.tracks.values() if track.length >= self.min_track_length]

def process_tracking_data(data_dir: str, output_dir: str):
    """Process pose estimation data for tracking"""
    print(f"Processing tracking data from: {data_dir}")
    print(f"Output directory: {output_dir}")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize tracker
    tracker = IntegratedFlyTracker(
        max_disappeared=15,
        max_distance=0.15,
        pose_weight=0.7,
        bbox_weight=0.3,
        min_track_length=5
    )
    
    # Get all label files and sort them
    label_files = []
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file.endswith('.txt'):
                label_files.append(os.path.join(root, file))
    
    # Sort files by frame number for proper sequence
    label_files.sort()
    
    print(f"Found {len(label_files)} label files")
    
    # Process each frame
    frame_data = []
    for i, label_file in enumerate(label_files):
        frame_id = os.path.basename(label_file).replace('.txt', '')
        
        # Parse detections
        detections = tracker.parse_yolo_pose_label(label_file, frame_id)
        
        # Update tracker
        active_tracks = tracker.update(detections)
        
        # Store frame data
        frame_data.append({
            'frame_id': frame_id,
            'frame_number': i,
            'num_detections': len(detections),
            'num_active_tracks': len(active_tracks)
        })
        
        if (i + 1) % 100 == 0:
            print(f"Processed {i + 1}/{len(label_files)} frames")
    
    # Get final results
    all_tracks = tracker.get_all_tracks()
    valid_tracks = tracker.get_valid_tracks()
    
    print(f"\nTracking Results:")
    print(f"Total tracks: {len(all_tracks)}")
    print(f"Valid tracks (≥{tracker.min_track_length} frames): {len(valid_tracks)}")
    print(f"Active tracks: {len([t for t in all_tracks if t.is_active])}")
    
    # Calculate statistics
    track_lengths = [track.length for track in valid_tracks]
    if track_lengths:
        avg_length = np.mean(track_lengths)
        max_length = max(track_lengths)
        min_length = min(track_lengths)
        print(f"Average track length: {avg_length:.2f} frames")
        print(f"Max track length: {max_length} frames")
        print(f"Min track length: {min_length} frames")
    
    # Save results
    save_tracking_results(valid_tracks, frame_data, output_dir)
    
    return valid_tracks, frame_data

def save_tracking_results(tracks: List[Track], frame_data: List[dict], output_dir: str):
    """Save tracking results to files"""
    
    # Save tracks summary
    tracks_data = []
    for track in tracks:
        tracks_data.append({
            'track_id': track.track_id,
            'length': track.length,
            'start_frame': track.start_frame,
            'last_seen': track.last_seen,
            'is_active': track.is_active
        })
    
    tracks_df = pd.DataFrame(tracks_data)
    tracks_df.to_csv(os.path.join(output_dir, 'tracks_summary.csv'), index=False)
    
    # Save frame-by-frame data
    frames_df = pd.DataFrame(frame_data)
    frames_df.to_csv(os.path.join(output_dir, 'frames_summary.csv'), index=False)
    
    # Save detailed trajectories
    trajectories = []
    for track in tracks:
        for detection in track.detections:
            trajectories.append({
                'track_id': track.track_id,
                'frame_id': detection.frame_id,
                'bbox_x': detection.bbox[0],
                'bbox_y': detection.bbox[1],
                'bbox_w': detection.bbox[2],
                'bbox_h': detection.bbox[3],
                'head_x': detection.keypoints[0][0] if len(detection.keypoints) > 0 else None,
                'head_y': detection.keypoints[0][1] if len(detection.keypoints) > 0 else None,
                'thorax_x': detection.keypoints[1][0] if len(detection.keypoints) > 1 else None,
                'thorax_y': detection.keypoints[1][1] if len(detection.keypoints) > 1 else None,
                'abdomen_x': detection.keypoints[2][0] if len(detection.keypoints) > 2 else None,
                'abdomen_y': detection.keypoints[2][1] if len(detection.keypoints) > 2 else None,
                'confidence': detection.confidence
            })
    
    trajectories_df = pd.DataFrame(trajectories)
    trajectories_df.to_csv(os.path.join(output_dir, 'trajectories.csv'), index=False)
    
    # Save tracking statistics
    stats = {
        'total_tracks': len(tracks),
        'active_tracks': len([t for t in tracks if t.is_active]),
        'avg_track_length': np.mean([t.length for t in tracks]) if tracks else 0,
        'max_track_length': max([t.length for t in tracks]) if tracks else 0,
        'min_track_length': min([t.length for t in tracks]) if tracks else 0,
        'total_frames': len(frame_data),
        'processing_time': datetime.now().isoformat()
    }
    
    with open(os.path.join(output_dir, 'tracking_stats.json'), 'w') as f:
        json.dump(stats, f, indent=2)
    
    print(f"\nResults saved to: {output_dir}")
    print(f"- tracks_summary.csv: {len(tracks)} tracks")
    print(f"- frames_summary.csv: {len(frame_data)} frames")
    print(f"- trajectories.csv: {len(trajectories)} detections")
    print(f"- tracking_stats.json: Statistics")

def main():
    parser = argparse.ArgumentParser(description='Integrated Fly Tracking Pipeline')
    parser.add_argument('--data_dir', 
                       default='/mnt/storage5/Fruitfly/Task2_ModelTraining/results/autolabeled_frames/autolabeled/labels',
                       help='Directory containing pose estimation label files')
    parser.add_argument('--output_dir',
                       default='/mnt/storage5/Fruitfly/Task3_FlyTracking/results/tracking_results',
                       help='Output directory for tracking results')
    parser.add_argument('--max_disappeared', type=int, default=15,
                       help='Maximum frames a track can be missing')
    parser.add_argument('--max_distance', type=float, default=0.15,
                       help='Maximum distance for track association')
    parser.add_argument('--min_track_length', type=int, default=5,
                       help='Minimum track length to consider valid')
    
    args = parser.parse_args()
    
    print("="*60)
    print("INTEGRATED FLY TRACKING PIPELINE")
    print("="*60)
    print(f"Data directory: {args.data_dir}")
    print(f"Output directory: {args.output_dir}")
    print(f"Max disappeared: {args.max_disappeared}")
    print(f"Max distance: {args.max_distance}")
    print(f"Min track length: {args.min_track_length}")
    print("="*60)
    
    # Process tracking
    tracks, frame_data = process_tracking_data(args.data_dir, args.output_dir)
    
    print("\n" + "="*60)
    print("TRACKING COMPLETE!")
    print("="*60)

if __name__ == "__main__":
    main()
