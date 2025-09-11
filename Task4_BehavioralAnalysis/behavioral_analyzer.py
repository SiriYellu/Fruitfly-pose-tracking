#!/usr/bin/env python3
"""
Behavioral Feature Extraction System for Task 4
Extracts behavioral metrics from tracked fly trajectories
"""

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
    """Container for behavioral metrics of a single fly"""
    track_id: int
    total_distance: float
    avg_speed: float
    max_speed: float
    movement_frequency: int  # Number of activity bouts
    stationary_duration: float
    time_in_regions: Dict[str, float]  # Time spent in different vial regions
    turning_frequency: float
    pose_variability: float
    activity_level: float

class BehavioralAnalyzer:
    """Analyzes fly behavior from tracking data"""
    
    def __init__(self, vial_regions: Optional[Dict[str, Tuple[float, float, float, float]]] = None):
        """
        Initialize analyzer with vial region definitions
        Regions are defined as (x_min, y_min, x_max, y_max) in normalized coordinates
        """
        if vial_regions is None:
            # Default vial regions (center, edges, etc.)
            self.vial_regions = {
                'center': (0.3, 0.3, 0.7, 0.7),
                'top': (0.0, 0.0, 1.0, 0.3),
                'bottom': (0.0, 0.7, 1.0, 1.0),
                'left': (0.0, 0.0, 0.3, 1.0),
                'right': (0.7, 0.0, 1.0, 1.0)
            }
        else:
            self.vial_regions = vial_regions
        
        self.speed_threshold = 0.01  # Minimum speed to consider as movement
        self.stationary_threshold = 0.005  # Speed below this is considered stationary
        self.activity_bout_min_duration = 5  # Minimum frames for activity bout
    
    def calculate_distance(self, pos1: Tuple[float, float], pos2: Tuple[float, float]) -> float:
        """Calculate Euclidean distance between two positions"""
        return np.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)
    
    def calculate_speed(self, positions: List[Tuple[float, float]], frame_rate: float = 30.0) -> List[float]:
        """Calculate instantaneous speed from position sequence"""
        speeds = []
        for i in range(1, len(positions)):
            dist = self.calculate_distance(positions[i-1], positions[i])
            speed = dist * frame_rate  # pixels per second (normalized)
            speeds.append(speed)
        return speeds
    
    def detect_activity_bouts(self, speeds: List[float]) -> List[Tuple[int, int]]:
        """Detect activity bouts (periods of sustained movement)"""
        bouts = []
        in_bout = False
        bout_start = 0
        
        for i, speed in enumerate(speeds):
            if speed > self.speed_threshold:
                if not in_bout:
                    bout_start = i
                    in_bout = True
            else:
                if in_bout:
                    bout_length = i - bout_start
                    if bout_length >= self.activity_bout_min_duration:
                        bouts.append((bout_start, i))
                    in_bout = False
        
        # Handle case where bout continues to end
        if in_bout:
            bout_length = len(speeds) - bout_start
            if bout_length >= self.activity_bout_min_duration:
                bouts.append((bout_start, len(speeds)))
        
        return bouts
    
    def calculate_turning_angle(self, pos1: Tuple[float, float], 
                              pos2: Tuple[float, float], 
                              pos3: Tuple[float, float]) -> float:
        """Calculate turning angle between three consecutive positions"""
        # Vector from pos1 to pos2
        v1 = (pos2[0] - pos1[0], pos2[1] - pos1[1])
        # Vector from pos2 to pos3
        v2 = (pos3[0] - pos2[0], pos3[1] - pos2[1])
        
        # Calculate angle between vectors
        dot_product = v1[0] * v2[0] + v1[1] * v2[1]
        mag1 = np.sqrt(v1[0]**2 + v1[1]**2)
        mag2 = np.sqrt(v2[0]**2 + v2[1]**2)
        
        if mag1 == 0 or mag2 == 0:
            return 0
        
        cos_angle = dot_product / (mag1 * mag2)
        cos_angle = np.clip(cos_angle, -1, 1)  # Avoid numerical errors
        angle = np.arccos(cos_angle)
        
        return np.degrees(angle)
    
    def calculate_pose_variability(self, keypoints_sequence: List[List[Tuple[float, float, float]]]) -> float:
        """Calculate pose variability over time"""
        if len(keypoints_sequence) < 2:
            return 0.0
        
        # Extract head position (first keypoint) for each frame
        head_positions = []
        for keypoints in keypoints_sequence:
            if keypoints and len(keypoints) > 0:
                head_x, head_y, visibility = keypoints[0]
                if visibility > 0.5:  # Only use visible keypoints
                    head_positions.append((head_x, head_y))
        
        if len(head_positions) < 2:
            return 0.0
        
        # Calculate standard deviation of head position
        x_coords = [pos[0] for pos in head_positions]
        y_coords = [pos[1] for pos in head_positions]
        
        x_std = np.std(x_coords)
        y_std = np.std(y_coords)
        
        return np.sqrt(x_std**2 + y_std**2)
    
    def get_region_for_position(self, x: float, y: float) -> str:
        """Determine which vial region a position belongs to"""
        for region_name, (x_min, y_min, x_max, y_max) in self.vial_regions.items():
            if x_min <= x <= x_max and y_min <= y <= y_max:
                return region_name
        return 'unknown'
    
    def analyze_trajectory(self, trajectory: Dict) -> BehavioralMetrics:
        """Analyze a single trajectory and extract behavioral metrics"""
        track_id = trajectory['track_id']
        keypoints_data = trajectory['keypoints']
        
        if len(keypoints_data) < 2:
            return BehavioralMetrics(
                track_id=track_id,
                total_distance=0.0,
                avg_speed=0.0,
                max_speed=0.0,
                movement_frequency=0,
                stationary_duration=0.0,
                time_in_regions={},
                turning_frequency=0.0,
                pose_variability=0.0,
                activity_level=0.0
            )
        
        # Extract positions (head keypoint)
        positions = []
        keypoints_sequence = []
        
        for frame_data in keypoints_data:
            keypoints = frame_data['keypoints']
            if keypoints and len(keypoints) > 0:
                head_x, head_y, visibility = keypoints[0]
                if visibility > 0.5:
                    positions.append((head_x, head_y))
                    keypoints_sequence.append(keypoints)
                else:
                    # Use bbox center if head not visible
                    bbox = frame_data['bbox']
                    positions.append((bbox[0], bbox[1]))
                    keypoints_sequence.append(keypoints)
        
        if len(positions) < 2:
            return BehavioralMetrics(
                track_id=track_id,
                total_distance=0.0,
                avg_speed=0.0,
                max_speed=0.0,
                movement_frequency=0,
                stationary_duration=0.0,
                time_in_regions={},
                turning_frequency=0.0,
                pose_variability=0.0,
                activity_level=0.0
            )
        
        # Calculate speeds
        speeds = self.calculate_speed(positions)
        
        # Basic movement metrics
        total_distance = sum(self.calculate_distance(positions[i-1], positions[i]) 
                           for i in range(1, len(positions)))
        avg_speed = np.mean(speeds) if speeds else 0.0
        max_speed = np.max(speeds) if speeds else 0.0
        
        # Activity bouts
        activity_bouts = self.detect_activity_bouts(speeds)
        movement_frequency = len(activity_bouts)
        
        # Stationary duration
        stationary_frames = sum(1 for speed in speeds if speed < self.stationary_threshold)
        stationary_duration = stationary_frames / 30.0  # Assuming 30 FPS
        
        # Time in regions
        time_in_regions = {region: 0.0 for region in self.vial_regions.keys()}
        for pos in positions:
            region = self.get_region_for_position(pos[0], pos[1])
            if region in time_in_regions:
                time_in_regions[region] += 1.0 / 30.0  # Assuming 30 FPS
        
        # Turning frequency
        turning_angles = []
        for i in range(2, len(positions)):
            angle = self.calculate_turning_angle(positions[i-2], positions[i-1], positions[i])
            turning_angles.append(angle)
        
        turning_frequency = len([a for a in turning_angles if a > 30]) / (len(positions) / 30.0)  # Turns per second
        
        # Pose variability
        pose_variability = self.calculate_pose_variability(keypoints_sequence)
        
        # Activity level (fraction of time spent moving)
        activity_level = sum(1 for speed in speeds if speed > self.speed_threshold) / len(speeds) if speeds else 0.0
        
        return BehavioralMetrics(
            track_id=track_id,
            total_distance=total_distance,
            avg_speed=avg_speed,
            max_speed=max_speed,
            movement_frequency=movement_frequency,
            stationary_duration=stationary_duration,
            time_in_regions=time_in_regions,
            turning_frequency=turning_frequency,
            pose_variability=pose_variability,
            activity_level=activity_level
        )

def load_trajectories(trajectories_file: str) -> List[Dict]:
    """Load trajectory data from JSON file"""
    with open(trajectories_file, 'r') as f:
        return json.load(f)

def analyze_all_trajectories(trajectories_file: str, output_dir: str):
    """Analyze all trajectories and generate behavioral reports"""
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Load trajectories
    trajectories = load_trajectories(trajectories_file)
    print(f"Loaded {len(trajectories)} trajectories")
    
    # Initialize analyzer
    analyzer = BehavioralAnalyzer()
    
    # Analyze each trajectory
    all_metrics = []
    for trajectory in trajectories:
        metrics = analyzer.analyze_trajectory(trajectory)
        all_metrics.append(metrics)
    
    # Convert to DataFrame
    metrics_data = []
    for metrics in all_metrics:
        row = {
            'track_id': metrics.track_id,
            'total_distance': metrics.total_distance,
            'avg_speed': metrics.avg_speed,
            'max_speed': metrics.max_speed,
            'movement_frequency': metrics.movement_frequency,
            'stationary_duration': metrics.stationary_duration,
            'turning_frequency': metrics.turning_frequency,
            'pose_variability': metrics.pose_variability,
            'activity_level': metrics.activity_level
        }
        
        # Add region times
        for region, time in metrics.time_in_regions.items():
            row[f'time_in_{region}'] = time
        
        metrics_data.append(row)
    
    df = pd.DataFrame(metrics_data)
    
    # Save detailed results
    df.to_csv(output_path / "behavioral_metrics.csv", index=False)
    
    # Generate summary statistics
    generate_summary_report(df, output_path)
    
    # Generate visualizations
    generate_behavioral_plots(df, output_path)
    
    print(f"Behavioral analysis complete! Results saved to {output_path}")
    print(f"Analyzed {len(df)} fly trajectories")

def generate_summary_report(df: pd.DataFrame, output_path: Path):
    """Generate summary statistics report"""
    summary = {
        'total_tracks': len(df),
        'analysis_timestamp': datetime.now().isoformat(),
        'summary_statistics': {}
    }
    
    # Calculate summary statistics for each metric
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    
    for col in numeric_columns:
        if col != 'track_id':
            summary['summary_statistics'][col] = {
                'mean': float(df[col].mean()),
                'std': float(df[col].std()),
                'min': float(df[col].min()),
                'max': float(df[col].max()),
                'median': float(df[col].median())
            }
    
    # Save summary
    with open(output_path / "behavioral_summary.json", 'w') as f:
        json.dump(summary, f, indent=2)
    
    # Print summary
    print("\n=== Behavioral Analysis Summary ===")
    print(f"Total tracks analyzed: {summary['total_tracks']}")
    print("\nKey Metrics (mean ± std):")
    for metric, stats in summary['summary_statistics'].items():
        if metric in ['total_distance', 'avg_speed', 'max_speed', 'activity_level']:
            print(f"  {metric}: {stats['mean']:.4f} ± {stats['std']:.4f}")

def generate_behavioral_plots(df: pd.DataFrame, output_path: Path):
    """Generate behavioral analysis plots"""
    plt.style.use('default')
    
    # Create figure with subplots
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle('Fly Behavioral Analysis', fontsize=16)
    
    # Speed distribution
    axes[0, 0].hist(df['avg_speed'], bins=30, alpha=0.7, color='skyblue')
    axes[0, 0].set_title('Average Speed Distribution')
    axes[0, 0].set_xlabel('Average Speed')
    axes[0, 0].set_ylabel('Frequency')
    
    # Distance traveled
    axes[0, 1].hist(df['total_distance'], bins=30, alpha=0.7, color='lightgreen')
    axes[0, 1].set_title('Total Distance Traveled')
    axes[0, 1].set_xlabel('Total Distance')
    axes[0, 1].set_ylabel('Frequency')
    
    # Activity level
    axes[0, 2].hist(df['activity_level'], bins=30, alpha=0.7, color='orange')
    axes[0, 2].set_title('Activity Level Distribution')
    axes[0, 2].set_xlabel('Activity Level')
    axes[0, 2].set_ylabel('Frequency')
    
    # Movement frequency
    axes[1, 0].hist(df['movement_frequency'], bins=30, alpha=0.7, color='pink')
    axes[1, 0].set_title('Movement Frequency')
    axes[1, 0].set_xlabel('Number of Activity Bouts')
    axes[1, 0].set_ylabel('Frequency')
    
    # Turning frequency
    axes[1, 1].hist(df['turning_frequency'], bins=30, alpha=0.7, color='purple')
    axes[1, 1].set_title('Turning Frequency')
    axes[1, 1].set_xlabel('Turns per Second')
    axes[1, 1].set_ylabel('Frequency')
    
    # Pose variability
    axes[1, 2].hist(df['pose_variability'], bins=30, alpha=0.7, color='brown')
    axes[1, 2].set_title('Pose Variability')
    axes[1, 2].set_xlabel('Pose Variability')
    axes[1, 2].set_ylabel('Frequency')
    
    plt.tight_layout()
    plt.savefig(output_path / "behavioral_analysis.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    # Region occupancy plot
    region_cols = [col for col in df.columns if col.startswith('time_in_')]
    if region_cols:
        region_data = df[region_cols].mean()
        region_data.plot(kind='bar', figsize=(10, 6))
        plt.title('Average Time Spent in Different Vial Regions')
        plt.xlabel('Vial Region')
        plt.ylabel('Time (seconds)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(output_path / "region_occupancy.png", dpi=300, bbox_inches='tight')
        plt.close()
    
    print("Generated behavioral analysis plots")

def main():
    parser = argparse.ArgumentParser(description='Behavioral Feature Extraction')
    parser.add_argument('--trajectories_file', type=str,
                       default='/mnt/storage5/Fruitfly/tracking_results/trajectories.json',
                       help='Path to trajectories JSON file')
    parser.add_argument('--output_dir', type=str,
                       default='/mnt/storage5/Fruitfly/behavioral_analysis',
                       help='Output directory for behavioral analysis')
    
    args = parser.parse_args()
    
    print("Starting Behavioral Analysis...")
    print(f"Trajectories file: {args.trajectories_file}")
    print(f"Output directory: {args.output_dir}")
    
    analyze_all_trajectories(args.trajectories_file, args.output_dir)

if __name__ == "__main__":
    main()
