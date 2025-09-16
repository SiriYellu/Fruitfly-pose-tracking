#!/usr/bin/env python3
"""
Behavioral Analysis for Task 3 Tracking Results
Analyzes tracked fly trajectories to extract behavioral metrics
"""

import os
import json
import numpy as np
import pandas as pd
from pathlib import Path
from typing import List, Dict, Tuple
import argparse
from datetime import datetime

def load_tracking_data(tracking_dir: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Load tracking results"""
    trajectories_file = os.path.join(tracking_dir, 'trajectories.csv')
    tracks_file = os.path.join(tracking_dir, 'tracks_summary.csv')
    
    if not os.path.exists(trajectories_file):
        raise FileNotFoundError(f"Trajectories file not found: {trajectories_file}")
    
    trajectories = pd.read_csv(trajectories_file)
    tracks_summary = pd.read_csv(tracks_file) if os.path.exists(tracks_file) else None
    
    return trajectories, tracks_summary

def calculate_behavioral_metrics(trajectories: pd.DataFrame) -> pd.DataFrame:
    """Calculate behavioral metrics for each track"""
    
    behavioral_data = []
    
    for track_id in trajectories['track_id'].unique():
        track_data = trajectories[trajectories['track_id'] == track_id].sort_values('frame_id')
        
        if len(track_data) < 2:
            continue
        
        # Calculate speeds
        speeds = []
        distances = []
        
        for i in range(1, len(track_data)):
            prev_row = track_data.iloc[i-1]
            curr_row = track_data.iloc[i]
            
            # Calculate distance between consecutive positions (using thorax as reference)
            if pd.notna(curr_row['thorax_x']) and pd.notna(curr_row['thorax_y']) and \
               pd.notna(prev_row['thorax_x']) and pd.notna(prev_row['thorax_y']):
                
                dx = curr_row['thorax_x'] - prev_row['thorax_x']
                dy = curr_row['thorax_y'] - prev_row['thorax_y']
                distance = np.sqrt(dx**2 + dy**2)
                distances.append(distance)
                
                # Speed (assuming 30 FPS)
                speed = distance * 30  # pixels per second
                speeds.append(speed)
        
        if not speeds:
            continue
        
        speeds = np.array(speeds)
        distances = np.array(distances)
        
        # Calculate metrics
        total_distance = np.sum(distances)
        avg_speed = np.mean(speeds)
        max_speed = np.max(speeds)
        
        # Activity level (proportion of time moving)
        movement_threshold = 0.01  # pixels per frame
        active_frames = np.sum(distances > movement_threshold)
        activity_level = active_frames / len(distances) if len(distances) > 0 else 0
        
        # Movement frequency (number of movement bouts)
        movement_bouts = 0
        in_movement = False
        for dist in distances:
            if dist > movement_threshold and not in_movement:
                movement_bouts += 1
                in_movement = True
            elif dist <= movement_threshold:
                in_movement = False
        
        # Pose variability (using head position)
        head_positions = track_data[['head_x', 'head_y']].dropna()
        if len(head_positions) > 1:
            head_std = np.std(head_positions.values, axis=0)
            pose_variability = np.mean(head_std)
        else:
            pose_variability = 0
        
        # Turning frequency (direction changes)
        if len(track_data) > 2:
            directions = []
            for i in range(1, len(track_data)):
                prev_row = track_data.iloc[i-1]
                curr_row = track_data.iloc[i]
                
                if pd.notna(curr_row['thorax_x']) and pd.notna(curr_row['thorax_y']) and \
                   pd.notna(prev_row['thorax_x']) and pd.notna(prev_row['thorax_y']):
                    
                    dx = curr_row['thorax_x'] - prev_row['thorax_x']
                    dy = curr_row['thorax_y'] - prev_row['thorax_y']
                    direction = np.arctan2(dy, dx)
                    directions.append(direction)
            
            if len(directions) > 1:
                direction_changes = 0
                for i in range(1, len(directions)):
                    angle_diff = abs(directions[i] - directions[i-1])
                    # Normalize angle difference
                    angle_diff = min(angle_diff, 2*np.pi - angle_diff)
                    if angle_diff > np.pi/4:  # 45 degrees
                        direction_changes += 1
                
                turning_frequency = direction_changes / len(directions) * 100  # per 100 frames
            else:
                turning_frequency = 0
        else:
            turning_frequency = 0
        
        # Spatial behavior (region occupancy)
        thorax_positions = track_data[['thorax_x', 'thorax_y']].dropna()
        if len(thorax_positions) > 0:
            # Define regions based on OVERALL data ranges (fixed for all tracks)
            # Use middle 60% of overall arena as center
            # These are the overall data ranges: X: 0.077-0.998, Y: 0.345-0.795
            overall_x_min, overall_x_max = 0.077, 0.998
            overall_y_min, overall_y_max = 0.345, 0.795
            
            overall_x_range = overall_x_max - overall_x_min
            overall_y_range = overall_y_max - overall_y_min
            
            # Center: middle 60% of overall arena
            center_x_min = overall_x_min + 0.2 * overall_x_range
            center_x_max = overall_x_max - 0.2 * overall_x_range
            center_y_min = overall_y_min + 0.2 * overall_y_range
            center_y_max = overall_y_max - 0.2 * overall_y_range
            
            # Corner: outer 20% on both dimensions
            corner_positions = thorax_positions[
                ((thorax_positions['thorax_x'] < center_x_min) | (thorax_positions['thorax_x'] > center_x_max)) &
                ((thorax_positions['thorax_y'] < center_y_min) | (thorax_positions['thorax_y'] > center_y_max))
            ]
            
            # Center: middle 60% of each dimension
            center_positions = thorax_positions[
                (thorax_positions['thorax_x'] >= center_x_min) & 
                (thorax_positions['thorax_x'] <= center_x_max) &
                (thorax_positions['thorax_y'] >= center_y_min) & 
                (thorax_positions['thorax_y'] <= center_y_max)
            ]
            
            # Edge: everything else (not center, not corner)
            edge_positions = thorax_positions[
                ~((thorax_positions['thorax_x'] >= center_x_min) & 
                  (thorax_positions['thorax_x'] <= center_x_max) &
                  (thorax_positions['thorax_y'] >= center_y_min) & 
                  (thorax_positions['thorax_y'] <= center_y_max)) &
                ~(((thorax_positions['thorax_x'] < center_x_min) | (thorax_positions['thorax_x'] > center_x_max)) &
                  ((thorax_positions['thorax_y'] < center_y_min) | (thorax_positions['thorax_y'] > center_y_max)))
            ]
            
            time_in_center = len(center_positions) / len(thorax_positions)
            time_in_edge = len(edge_positions) / len(thorax_positions)
            time_in_corner = len(corner_positions) / len(thorax_positions)
        else:
            time_in_center = 0
            time_in_edge = 0
            time_in_corner = 0
        
        # Calculate stationary duration
        duration = len(track_data) / 30.0  # seconds at 30 FPS
        stationary_duration = (1 - activity_level) * duration
        
        behavioral_data.append({
            'track_id': track_id,
            'total_distance': total_distance,
            'avg_speed': avg_speed,
            'max_speed': max_speed,
            'activity_level': activity_level,
            'movement_frequency': movement_bouts,
            'stationary_duration': stationary_duration,
            'pose_variability': pose_variability,
            'turning_frequency': turning_frequency,
            'time_in_center': time_in_center,
            'time_in_edge': time_in_edge,
            'time_in_corner': time_in_corner,
            'track_length': len(track_data),
            'duration': duration
        })
    
    return pd.DataFrame(behavioral_data)

def save_behavioral_results(behavioral_df: pd.DataFrame, output_dir: str):
    """Save behavioral analysis results"""
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Save detailed metrics
    behavioral_df.to_csv(os.path.join(output_dir, 'behavioral_metrics.csv'), index=False)
    
    # Calculate summary statistics
    summary_stats = {}
    for column in behavioral_df.columns:
        if column != 'track_id':
            summary_stats[column] = {
                'mean': float(behavioral_df[column].mean()),
                'std': float(behavioral_df[column].std()),
                'min': float(behavioral_df[column].min()),
                'max': float(behavioral_df[column].max()),
                'median': float(behavioral_df[column].median())
            }
    
    # Save summary
    with open(os.path.join(output_dir, 'behavioral_summary.json'), 'w') as f:
        json.dump({
            'total_tracks': len(behavioral_df),
            'analysis_timestamp': datetime.now().isoformat(),
            'summary_statistics': summary_stats
        }, f, indent=2)
    
    print(f"Behavioral analysis results saved to: {output_dir}")
    print(f"- behavioral_metrics.csv: {len(behavioral_df)} tracks")
    print(f"- behavioral_summary.json: Summary statistics")

def main():
    parser = argparse.ArgumentParser(description='Behavioral Analysis for Tracking Results')
    parser.add_argument('--tracking_dir',
                       default='/mnt/storage5/Fruitfly/Task3_FlyTracking/results/tracking_results',
                       help='Directory containing tracking results')
    parser.add_argument('--output_dir',
                       default='/mnt/storage5/Fruitfly/Task3_FlyTracking/results/behavioral_analysis',
                       help='Output directory for behavioral analysis')
    
    args = parser.parse_args()
    
    print("="*60)
    print("BEHAVIORAL ANALYSIS FOR TRACKING RESULTS")
    print("="*60)
    print(f"Tracking directory: {args.tracking_dir}")
    print(f"Output directory: {args.output_dir}")
    print("="*60)
    
    # Load tracking data
    print("Loading tracking data...")
    trajectories, tracks_summary = load_tracking_data(args.tracking_dir)
    print(f"Loaded {len(trajectories)} trajectory points from {trajectories['track_id'].nunique()} tracks")
    
    # Calculate behavioral metrics
    print("Calculating behavioral metrics...")
    behavioral_df = calculate_behavioral_metrics(trajectories)
    print(f"Calculated metrics for {len(behavioral_df)} tracks")
    
    # Save results
    save_behavioral_results(behavioral_df, args.output_dir)
    
    # Print summary
    print("\n" + "="*60)
    print("BEHAVIORAL ANALYSIS SUMMARY")
    print("="*60)
    print(f"Total tracks analyzed: {len(behavioral_df)}")
    print(f"Average distance: {behavioral_df['total_distance'].mean():.4f} ± {behavioral_df['total_distance'].std():.4f}")
    print(f"Average speed: {behavioral_df['avg_speed'].mean():.4f} ± {behavioral_df['avg_speed'].std():.4f}")
    print(f"Activity level: {behavioral_df['activity_level'].mean():.4f} ± {behavioral_df['activity_level'].std():.4f}")
    print(f"Movement frequency: {behavioral_df['movement_frequency'].mean():.4f} ± {behavioral_df['movement_frequency'].std():.4f}")
    print(f"Time in center: {behavioral_df['time_in_center'].mean():.4f} ± {behavioral_df['time_in_center'].std():.4f}")
    print(f"Time in edge: {behavioral_df['time_in_edge'].mean():.4f} ± {behavioral_df['time_in_edge'].std():.4f}")
    print("="*60)

if __name__ == "__main__":
    main()
