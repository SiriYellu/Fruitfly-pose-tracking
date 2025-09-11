#!/usr/bin/env python3
"""
Behavioral Feature Extraction for Task 4
Extracts comprehensive behavioral metrics from tracked fly data
"""

import os
import json
import numpy as np
import pandas as pd
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import argparse

@dataclass
class BehavioralMetrics:
    """Container for behavioral metrics for a single fly"""
    track_id: int
    total_distance: float
    average_speed: float
    max_speed: float
    movement_frequency: int
    stationary_duration: float
    activity_level: float
    turning_frequency: float
    pose_variability: float
    time_in_center: float
    time_in_edge: float
    time_in_corner: float
    trajectory_length: int
    start_time: str
    end_time: str
    duration: float

class BehavioralAnalyzer:
    """Analyzes behavioral patterns from tracked fly data"""
    
    def __init__(self, 
                 frame_rate: float = 30.0,
                 pixel_to_mm: float = 0.1,  # Conversion factor
                 activity_threshold: float = 0.5,  # mm/s
                 stationary_threshold: float = 0.1,  # mm/s
                 turn_threshold: float = 30.0):  # degrees
        self.frame_rate = frame_rate
        self.pixel_to_mm = pixel_to_mm
        self.activity_threshold = activity_threshold
        self.stationary_threshold = stationary_threshold
        self.turn_threshold = turn_threshold
        
    def calculate_distance(self, point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
        """Calculate Euclidean distance between two points in mm"""
        dx = (point1[0] - point2[0]) * self.pixel_to_mm
        dy = (point1[1] - point2[1]) * self.pixel_to_mm
        return np.sqrt(dx**2 + dy**2)
    
    def calculate_speed(self, positions: List[Tuple[float, float]], time_window: int = 1) -> List[float]:
        """Calculate instantaneous speed for each position"""
        speeds = []
        for i in range(len(positions)):
            if i < time_window:
                speeds.append(0.0)
            else:
                dist = self.calculate_distance(positions[i], positions[i-time_window])
                time_diff = time_window / self.frame_rate
                speed = dist / time_diff if time_diff > 0 else 0.0
                speeds.append(speed)
        return speeds
    
    def calculate_turning_angle(self, p1: Tuple[float, float], 
                               p2: Tuple[float, float], 
                               p3: Tuple[float, float]) -> float:
        """Calculate turning angle between three consecutive points"""
        # Vector from p1 to p2
        v1 = np.array([p2[0] - p1[0], p2[1] - p1[1]])
        # Vector from p2 to p3
        v2 = np.array([p3[0] - p2[0], p3[1] - p2[1]])
        
        # Calculate angle between vectors
        cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-8)
        cos_angle = np.clip(cos_angle, -1.0, 1.0)
        angle = np.arccos(cos_angle)
        
        # Convert to degrees
        return np.degrees(angle)
    
    def calculate_pose_variability(self, keypoints_list: List[List[Tuple[float, float, float]]]) -> float:
        """Calculate pose variability across frames"""
        if len(keypoints_list) < 2:
            return 0.0
        
        # Extract head positions (first keypoint)
        head_positions = []
        for keypoints in keypoints_list:
            if keypoints and len(keypoints) > 0:
                head_positions.append((keypoints[0][0], keypoints[0][1]))
        
        if len(head_positions) < 2:
            return 0.0
        
        # Calculate variance in head position
        head_x = [pos[0] for pos in head_positions]
        head_y = [pos[1] for pos in head_positions]
        
        variance_x = np.var(head_x)
        variance_y = np.var(head_y)
        
        return np.sqrt(variance_x + variance_y)
    
    def classify_region(self, position: Tuple[float, float], image_width: float = 640, image_height: float = 480) -> str:
        """Classify position into vial regions"""
        x, y = position
        x_norm = x / image_width
        y_norm = y / image_height
        
        # Define regions (adjust based on your vial setup)
        if 0.2 <= x_norm <= 0.8 and 0.2 <= y_norm <= 0.8:
            return "center"
        elif x_norm < 0.2 or x_norm > 0.8 or y_norm < 0.2 or y_norm > 0.8:
            return "edge"
        else:
            return "corner"
    
    def analyze_track(self, track_data: Dict) -> BehavioralMetrics:
        """Analyze behavioral metrics for a single track"""
        track_id = track_data['track_id']
        keypoints_data = track_data['keypoints']
        
        if len(keypoints_data) < 3:
            # Return empty metrics for short tracks
            return BehavioralMetrics(
                track_id=track_id,
                total_distance=0.0,
                average_speed=0.0,
                max_speed=0.0,
                movement_frequency=0,
                stationary_duration=0.0,
                activity_level=0.0,
                turning_frequency=0.0,
                pose_variability=0.0,
                time_in_center=0.0,
                time_in_edge=0.0,
                time_in_corner=0.0,
                trajectory_length=len(keypoints_data),
                start_time=keypoints_data[0]['frame_id'] if keypoints_data else "",
                end_time=keypoints_data[-1]['frame_id'] if keypoints_data else "",
                duration=len(keypoints_data) / self.frame_rate
            )
        
        # Extract positions (using head keypoint - first keypoint)
        positions = []
        keypoints_list = []
        region_counts = {"center": 0, "edge": 0, "corner": 0}
        
        for frame_data in keypoints_data:
            keypoints = frame_data['keypoints']
            if keypoints and len(keypoints) > 0:
                # Use head position (first keypoint)
                head_pos = (keypoints[0][0], keypoints[0][1])
                positions.append(head_pos)
                keypoints_list.append(keypoints)
                
                # Classify region
                region = self.classify_region(head_pos)
                region_counts[region] += 1
        
        if len(positions) < 2:
            return BehavioralMetrics(
                track_id=track_id,
                total_distance=0.0,
                average_speed=0.0,
                max_speed=0.0,
                movement_frequency=0,
                stationary_duration=0.0,
                activity_level=0.0,
                turning_frequency=0.0,
                pose_variability=0.0,
                time_in_center=0.0,
                time_in_edge=0.0,
                time_in_corner=0.0,
                trajectory_length=len(positions),
                start_time=keypoints_data[0]['frame_id'] if keypoints_data else "",
                end_time=keypoints_data[-1]['frame_id'] if keypoints_data else "",
                duration=len(positions) / self.frame_rate
            )
        
        # Calculate distances and speeds
        distances = []
        for i in range(1, len(positions)):
            dist = self.calculate_distance(positions[i-1], positions[i])
            distances.append(dist)
        
        total_distance = sum(distances)
        speeds = self.calculate_speed(positions)
        average_speed = np.mean(speeds) if speeds else 0.0
        max_speed = np.max(speeds) if speeds else 0.0
        
        # Calculate movement frequency (number of active periods)
        movement_frequency = 0
        stationary_duration = 0.0
        in_movement = False
        
        for speed in speeds:
            if speed > self.activity_threshold:
                if not in_movement:
                    movement_frequency += 1
                    in_movement = True
            else:
                if in_movement:
                    in_movement = False
                if speed < self.stationary_threshold:
                    stationary_duration += 1.0 / self.frame_rate
        
        # Calculate activity level (proportion of time moving)
        active_frames = sum(1 for speed in speeds if speed > self.activity_threshold)
        activity_level = active_frames / len(speeds) if speeds else 0.0
        
        # Calculate turning frequency
        turning_angles = []
        for i in range(2, len(positions)):
            angle = self.calculate_turning_angle(positions[i-2], positions[i-1], positions[i])
            turning_angles.append(angle)
        
        turning_frequency = sum(1 for angle in turning_angles if angle > self.turn_threshold) / len(turning_angles) if turning_angles else 0.0
        
        # Calculate pose variability
        pose_variability = self.calculate_pose_variability(keypoints_list)
        
        # Calculate time in each region
        total_frames = len(positions)
        time_in_center = region_counts["center"] / total_frames if total_frames > 0 else 0.0
        time_in_edge = region_counts["edge"] / total_frames if total_frames > 0 else 0.0
        time_in_corner = region_counts["corner"] / total_frames if total_frames > 0 else 0.0
        
        return BehavioralMetrics(
            track_id=track_id,
            total_distance=total_distance,
            average_speed=average_speed,
            max_speed=max_speed,
            movement_frequency=movement_frequency,
            stationary_duration=stationary_duration,
            activity_level=activity_level,
            turning_frequency=turning_frequency,
            pose_variability=pose_variability,
            time_in_center=time_in_center,
            time_in_edge=time_in_edge,
            time_in_corner=time_in_corner,
            trajectory_length=len(positions),
            start_time=keypoints_data[0]['frame_id'] if keypoints_data else "",
            end_time=keypoints_data[-1]['frame_id'] if keypoints_data else "",
            duration=len(positions) / self.frame_rate
        )
    
    def analyze_all_tracks(self, trajectories_file: str) -> List[BehavioralMetrics]:
        """Analyze behavioral metrics for all tracks"""
        print("Loading trajectory data...")
        
        with open(trajectories_file, 'r') as f:
            trajectories = json.load(f)
        
        print(f"Analyzing {len(trajectories)} tracks...")
        
        all_metrics = []
        for i, track_data in enumerate(trajectories):
            if i % 50 == 0:
                print(f"  Processing track {i+1}/{len(trajectories)}")
            
            metrics = self.analyze_track(track_data)
            all_metrics.append(metrics)
        
        print("Behavioral analysis complete!")
        return all_metrics
    
    def generate_summary_statistics(self, metrics: List[BehavioralMetrics]) -> Dict:
        """Generate summary statistics for all tracks"""
        if not metrics:
            return {}
        
        # Convert to DataFrame for easier analysis
        data = []
        for m in metrics:
            data.append({
                'track_id': m.track_id,
                'total_distance': m.total_distance,
                'average_speed': m.average_speed,
                'max_speed': m.max_speed,
                'movement_frequency': m.movement_frequency,
                'stationary_duration': m.stationary_duration,
                'activity_level': m.activity_level,
                'turning_frequency': m.turning_frequency,
                'pose_variability': m.pose_variability,
                'time_in_center': m.time_in_center,
                'time_in_edge': m.time_in_edge,
                'time_in_corner': m.time_in_corner,
                'trajectory_length': m.trajectory_length,
                'duration': m.duration
            })
        
        df = pd.DataFrame(data)
        
        summary = {
            'total_tracks': len(metrics),
            'total_distance_mean': df['total_distance'].mean(),
            'total_distance_std': df['total_distance'].std(),
            'average_speed_mean': df['average_speed'].mean(),
            'average_speed_std': df['average_speed'].std(),
            'max_speed_mean': df['max_speed'].mean(),
            'max_speed_std': df['max_speed'].std(),
            'movement_frequency_mean': df['movement_frequency'].mean(),
            'movement_frequency_std': df['movement_frequency'].std(),
            'stationary_duration_mean': df['stationary_duration'].mean(),
            'stationary_duration_std': df['stationary_duration'].std(),
            'activity_level_mean': df['activity_level'].mean(),
            'activity_level_std': df['activity_level'].std(),
            'turning_frequency_mean': df['turning_frequency'].mean(),
            'turning_frequency_std': df['turning_frequency'].std(),
            'pose_variability_mean': df['pose_variability'].mean(),
            'pose_variability_std': df['pose_variability'].std(),
            'time_in_center_mean': df['time_in_center'].mean(),
            'time_in_center_std': df['time_in_center'].std(),
            'time_in_edge_mean': df['time_in_edge'].mean(),
            'time_in_edge_std': df['time_in_edge'].std(),
            'time_in_corner_mean': df['time_in_corner'].mean(),
            'time_in_corner_std': df['time_in_corner'].std(),
            'trajectory_length_mean': df['trajectory_length'].mean(),
            'trajectory_length_std': df['trajectory_length'].std(),
            'duration_mean': df['duration'].mean(),
            'duration_std': df['duration'].std()
        }
        
        return summary
    
    def save_metrics(self, metrics: List[BehavioralMetrics], output_dir: str):
        """Save behavioral metrics to files"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Convert to DataFrame
        data = []
        for m in metrics:
            data.append({
                'track_id': m.track_id,
                'total_distance_mm': m.total_distance,
                'average_speed_mm_s': m.average_speed,
                'max_speed_mm_s': m.max_speed,
                'movement_frequency': m.movement_frequency,
                'stationary_duration_s': m.stationary_duration,
                'activity_level': m.activity_level,
                'turning_frequency': m.turning_frequency,
                'pose_variability': m.pose_variability,
                'time_in_center': m.time_in_center,
                'time_in_edge': m.time_in_edge,
                'time_in_corner': m.time_in_corner,
                'trajectory_length': m.trajectory_length,
                'start_time': m.start_time,
                'end_time': m.end_time,
                'duration_s': m.duration
            })
        
        df = pd.DataFrame(data)
        
        # Save detailed metrics
        df.to_csv(output_path / "behavioral_metrics_detailed.csv", index=False)
        
        # Save summary statistics
        summary = self.generate_summary_statistics(metrics)
        with open(output_path / "behavioral_summary.json", 'w') as f:
            json.dump(summary, f, indent=2)
        
        # Save summary as CSV
        summary_df = pd.DataFrame([summary])
        summary_df.to_csv(output_path / "behavioral_summary.csv", index=False)
        
        print(f"Behavioral metrics saved to {output_path}")
        print(f"Total tracks analyzed: {len(metrics)}")
        
        return summary

def main():
    parser = argparse.ArgumentParser(description='Behavioral Feature Extraction')
    parser.add_argument('--trajectories_file', type=str,
                       default='/mnt/storage5/Fruitfly/Task3_FlyTracking/results/tracking_results/trajectories.json',
                       help='Path to trajectories JSON file')
    parser.add_argument('--output_dir', type=str,
                       default='/mnt/storage5/Fruitfly/Task4_BehavioralAnalysis/results',
                       help='Output directory for behavioral analysis')
    parser.add_argument('--frame_rate', type=float, default=30.0,
                       help='Frame rate of the video')
    parser.add_argument('--pixel_to_mm', type=float, default=0.1,
                       help='Pixel to millimeter conversion factor')
    
    args = parser.parse_args()
    
    print("Starting Behavioral Feature Extraction...")
    print(f"Trajectories file: {args.trajectories_file}")
    print(f"Output directory: {args.output_dir}")
    
    # Initialize analyzer
    analyzer = BehavioralAnalyzer(
        frame_rate=args.frame_rate,
        pixel_to_mm=args.pixel_to_mm
    )
    
    # Analyze all tracks
    metrics = analyzer.analyze_all_tracks(args.trajectories_file)
    
    # Save results
    summary = analyzer.save_metrics(metrics, args.output_dir)
    
    print("\nBehavioral Analysis Summary:")
    print(f"  Total tracks: {summary['total_tracks']}")
    print(f"  Average distance: {summary['total_distance_mean']:.2f} ± {summary['total_distance_std']:.2f} mm")
    print(f"  Average speed: {summary['average_speed_mean']:.2f} ± {summary['average_speed_std']:.2f} mm/s")
    print(f"  Activity level: {summary['activity_level_mean']:.2f} ± {summary['activity_level_std']:.2f}")
    print(f"  Movement frequency: {summary['movement_frequency_mean']:.2f} ± {summary['movement_frequency_std']:.2f}")

if __name__ == "__main__":
    main()


