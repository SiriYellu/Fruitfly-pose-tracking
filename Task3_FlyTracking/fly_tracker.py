#!/usr/bin/env python3
"""
Fly Tracking System for Task 3
Implements multi-object tracking to associate detected flies across frames
Handles fly re-entry, partial occlusion, and ID reassignment
"""

import os
import cv2
import numpy as np
import pandas as pd
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from collections import defaultdict
import json
import argparse
from datetime import datetime

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
    
    @property
    def length(self):
        return len(self.detections)
    
    @property
    def last_detection(self):
        return self.detections[-1] if self.detections else None

class FlyTracker:
    """Multi-object tracker for flies using pose-based association"""
    
    def __init__(self, 
                 max_disappeared: int = 10,
                 max_distance: float = 0.1,
                 pose_weight: float = 0.7,
                 bbox_weight: float = 0.3,
                 min_track_length: int = 3):
        self.max_disappeared = max_disappeared
        self.max_distance = max_distance
        self.pose_weight = pose_weight
        self.bbox_weight = bbox_weight
        self.min_track_length = min_track_length
        
        self.tracks: Dict[int, Track] = {}
        self.next_track_id = 0
        self.frame_count = 0
        
    def _calculate_distance(self, det1: Detection, det2: Detection) -> float:
        """Calculate distance between two detections using pose and bbox"""
        # Pose distance (weighted by visibility)
        pose_dist = 0.0
        valid_keypoints = 0
        
        for (x1, y1, v1), (x2, y2, v2) in zip(det1.keypoints, det2.keypoints):
            if v1 > 0.5 and v2 > 0.5:  # Only use visible keypoints
                pose_dist += np.sqrt((x1 - x2)**2 + (y1 - y2)**2)
                valid_keypoints += 1
        
        if valid_keypoints > 0:
            pose_dist /= valid_keypoints
        else:
            pose_dist = 1.0  # Max distance if no valid keypoints
        
        # Bbox distance (center point)
        bbox_dist = np.sqrt(
            (det1.bbox[0] - det2.bbox[0])**2 + 
            (det1.bbox[1] - det2.bbox[1])**2
        )
        
        # Weighted combination
        return self.pose_weight * pose_dist + self.bbox_weight * bbox_dist
    
    def _associate_detections(self, detections: List[Detection]) -> Tuple[List[Detection], List[Detection]]:
        """Associate detections with existing tracks using Hungarian algorithm"""
        if not self.tracks or not detections:
            return [], detections
        
        # Create cost matrix
        active_tracks = [t for t in self.tracks.values() if t.is_active and t.last_detection]
        if not active_tracks:
            return [], detections
        
        cost_matrix = np.zeros((len(active_tracks), len(detections)))
        
        for i, track in enumerate(active_tracks):
            for j, detection in enumerate(detections):
                cost_matrix[i, j] = self._calculate_distance(track.last_detection, detection)
        
        # Simple greedy assignment (can be replaced with Hungarian algorithm)
        assigned_detections = []
        unassigned_detections = []
        
        used_tracks = set()
        used_detections = set()
        
        # Sort by cost
        assignments = []
        for i in range(len(active_tracks)):
            for j in range(len(detections)):
                if cost_matrix[i, j] < self.max_distance:
                    assignments.append((cost_matrix[i, j], i, j))
        
        assignments.sort()
        
        for cost, track_idx, det_idx in assignments:
            if track_idx not in used_tracks and det_idx not in used_detections:
                track = active_tracks[track_idx]
                detection = detections[det_idx]
                detection.track_id = track.track_id
                track.detections.append(detection)
                track.last_seen = self.frame_count
                assigned_detections.append(detection)
                used_tracks.add(track_idx)
                used_detections.add(det_idx)
        
        # Unassigned detections
        for j, detection in enumerate(detections):
            if j not in used_detections:
                unassigned_detections.append(detection)
        
        return assigned_detections, unassigned_detections
    
    def _create_new_tracks(self, detections: List[Detection]):
        """Create new tracks for unassigned detections"""
        for detection in detections:
            track = Track(
                track_id=self.next_track_id,
                detections=[detection],
                last_seen=self.frame_count
            )
            detection.track_id = self.next_track_id
            self.tracks[self.next_track_id] = track
            self.next_track_id += 1
    
    def _update_track_states(self):
        """Update track states and remove inactive tracks"""
        tracks_to_remove = []
        
        for track_id, track in self.tracks.items():
            if not track.is_active:
                continue
                
            # Check if track has been missing too long
            if self.frame_count - track.last_seen > self.max_disappeared:
                track.is_active = False
                if track.length < self.min_track_length:
                    tracks_to_remove.append(track_id)
        
        for track_id in tracks_to_remove:
            del self.tracks[track_id]
    
    def update(self, detections: List[Detection]) -> List[Track]:
        """Update tracker with new detections"""
        self.frame_count += 1
        
        # Associate detections with existing tracks
        assigned_detections, unassigned_detections = self._associate_detections(detections)
        
        # Create new tracks for unassigned detections
        self._create_new_tracks(unassigned_detections)
        
        # Update track states
        self._update_track_states()
        
        return [track for track in self.tracks.values() if track.is_active]
    
    def save_results(self, output_dir: str):
        """Save tracking results to output directory"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Generate trajectory data
        generate_trajectory_data(self, output_path)
        
        # Generate tracking statistics
        generate_tracking_stats(self, output_path)
        
        print(f"Tracking results saved to {output_path}")
        print(f"Total tracks: {len(self.tracks)}")
        print(f"Active tracks: {sum(1 for t in self.tracks.values() if t.is_active)}")

def parse_yolo_pose_label(label_path: str, frame_id: str) -> List[Detection]:
    """Parse YOLO pose label file and return detections"""
    detections = []
    
    if not os.path.exists(label_path):
        return detections
    
    with open(label_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            parts = line.split()
            if len(parts) < 13:  # class + bbox + 3 keypoints * 3 values
                continue
            
            try:
                # Parse class and bbox
                class_id = int(parts[0])
                bbox = (float(parts[1]), float(parts[2]), float(parts[3]), float(parts[4]))
                
                # Parse keypoints (3 keypoints, each with x, y, visibility)
                keypoints = []
                for i in range(3):
                    x = float(parts[5 + i*3])
                    y = float(parts[6 + i*3])
                    v = float(parts[7 + i*3])
                    keypoints.append((x, y, v))
                
                detection = Detection(
                    frame_id=frame_id,
                    bbox=bbox,
                    keypoints=keypoints,
                    confidence=1.0
                )
                detections.append(detection)
                
            except (ValueError, IndexError) as e:
                print(f"Error parsing line in {label_path}: {line}")
                continue
    
    return detections

def extract_frame_info(filename: str) -> Tuple[str, int, int]:
    """Extract date, segment, and frame number from filename"""
    # Format: run_YYMMDD_segXXX_frameYYYYY.jpg
    parts = filename.replace('.jpg', '').split('_')
    if len(parts) >= 4:
        date = parts[1]  # YYMMDD
        segment = int(parts[2].replace('seg', ''))
        frame = int(parts[3].replace('frame', ''))
        return date, segment, frame
    return "unknown", 0, 0

def process_tracking_data(data_dir: str, output_dir: str):
    """Process all tracking data and generate trajectories"""
    data_path = Path(data_dir)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Initialize tracker
    tracker = FlyTracker(
        max_disappeared=5,  # Allow 5 frames of missing data
        max_distance=0.15,  # Maximum distance for association
        pose_weight=0.8,    # Weight for pose similarity
        bbox_weight=0.2,    # Weight for bbox similarity
        min_track_length=3  # Minimum track length to keep
    )
    
    # Get all label files and sort by frame number
    label_files = list(data_path.glob("labels/*.txt"))
    frame_data = []
    
    for label_file in label_files:
        frame_id = label_file.stem
        date, segment, frame_num = extract_frame_info(frame_id)
        frame_data.append((frame_num, date, segment, frame_id, label_file))
    
    # Sort by frame number for temporal ordering
    frame_data.sort(key=lambda x: x[0])
    
    print(f"Processing {len(frame_data)} frames...")
    
    all_tracks = []
    frame_tracks = []
    
    # Process each frame
    for frame_num, date, segment, frame_id, label_file in frame_data:
        detections = parse_yolo_pose_label(str(label_file), frame_id)
        tracks = tracker.update(detections)
        
        frame_tracks.append({
            'frame_num': frame_num,
            'date': date,
            'segment': segment,
            'frame_id': frame_id,
            'num_detections': len(detections),
            'num_tracks': len(tracks)
        })
        
        # Collect all tracks
        for track in tracks:
            all_tracks.append({
                'track_id': track.track_id,
                'frame_num': frame_num,
                'date': date,
                'segment': segment,
                'frame_id': frame_id,
                'length': track.length,
                'is_active': track.is_active
            })
    
    # Save results
    tracks_df = pd.DataFrame(all_tracks)
    frames_df = pd.DataFrame(frame_tracks)
    
    tracks_df.to_csv(output_path / "tracks_summary.csv", index=False)
    frames_df.to_csv(output_path / "frames_summary.csv", index=False)
    
    # Generate detailed trajectory data
    generate_trajectory_data(tracker, output_path)
    
    # Generate tracking statistics
    generate_tracking_stats(tracker, output_path)
    
    print(f"Tracking complete! Results saved to {output_path}")
    print(f"Total tracks: {len(tracker.tracks)}")
    print(f"Active tracks: {sum(1 for t in tracker.tracks.values() if t.is_active)}")

def generate_trajectory_data(tracker: FlyTracker, output_path: Path):
    """Generate detailed trajectory data for each track"""
    trajectories = []
    
    for track_id, track in tracker.tracks.items():
        if track.length < 3:  # Skip short tracks
            continue
            
        trajectory = {
            'track_id': track_id,
            'length': track.length,
            'start_frame': track.detections[0].frame_id,
            'end_frame': track.detections[-1].frame_id,
            'keypoints': []
        }
        
        for detection in track.detections:
            frame_data = {
                'frame_id': detection.frame_id,
                'bbox': detection.bbox,
                'keypoints': detection.keypoints
            }
            trajectory['keypoints'].append(frame_data)
        
        trajectories.append(trajectory)
    
    # Save trajectories
    with open(output_path / "trajectories.json", 'w') as f:
        json.dump(trajectories, f, indent=2)
    
    print(f"Generated {len(trajectories)} trajectories")

def generate_tracking_stats(tracker: FlyTracker, output_path: Path):
    """Generate tracking statistics and visualizations"""
    stats = {
        'total_tracks': len(tracker.tracks),
        'active_tracks': sum(1 for t in tracker.tracks.values() if t.is_active),
        'track_lengths': [t.length for t in tracker.tracks.values()],
        'processing_time': datetime.now().isoformat()
    }
    
    if stats['track_lengths']:
        stats['avg_track_length'] = np.mean(stats['track_lengths'])
        stats['max_track_length'] = max(stats['track_lengths'])
        stats['min_track_length'] = min(stats['track_lengths'])
    
    with open(output_path / "tracking_stats.json", 'w') as f:
        json.dump(stats, f, indent=2)
    
    print(f"Tracking Statistics:")
    print(f"  Total tracks: {stats['total_tracks']}")
    print(f"  Active tracks: {stats['active_tracks']}")
    if stats['track_lengths']:
        print(f"  Average track length: {stats['avg_track_length']:.2f}")
        print(f"  Max track length: {stats['max_track_length']}")
        print(f"  Min track length: {stats['min_track_length']}")

def main():
    parser = argparse.ArgumentParser(description='Fly Tracking System')
    parser.add_argument('--data_dir', type=str, 
                       default='/mnt/storage5/Fruitfly/runs/autolabel_v4',
                       help='Directory containing labeled data')
    parser.add_argument('--output_dir', type=str,
                       default='/mnt/storage5/Fruitfly/tracking_results',
                       help='Output directory for tracking results')
    
    args = parser.parse_args()
    
    print("Starting Fly Tracking System...")
    print(f"Data directory: {args.data_dir}")
    print(f"Output directory: {args.output_dir}")
    
    process_tracking_data(args.data_dir, args.output_dir)

if __name__ == "__main__":
    main()
