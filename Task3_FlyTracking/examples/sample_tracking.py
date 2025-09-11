#!/usr/bin/env python3
"""
Sample usage examples for Task 3 Fly Tracking
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fly_tracker import FlyTracker, parse_yolo_pose_label
import numpy as np

def basic_tracking_example():
    """Basic tracking example"""
    print("=== Basic Tracking Example ===")
    
    # Initialize tracker
    tracker = FlyTracker(
        max_disappeared=10,
        max_distance=0.1,
        pose_weight=0.7,
        bbox_weight=0.3
    )
    
    # Simulate some detections
    detections = [
        # Frame 1: Two flies detected
        parse_yolo_pose_label("sample_frame1.txt", "frame1"),
        parse_yolo_pose_label("sample_frame2.txt", "frame2"),
    ]
    
    # Process detections
    for i, detection in enumerate(detections):
        tracks = tracker.update(detection)
        print(f"Frame {i+1}: {len(tracks)} active tracks")
        
        for track in tracks:
            print(f"  Track {track.track_id}: {track.length} frames")

def advanced_configuration_example():
    """Advanced configuration example"""
    print("\n=== Advanced Configuration Example ===")
    
    # Custom tracker configuration
    tracker = FlyTracker(
        max_disappeared=15,      # Allow longer gaps
        max_distance=0.08,       # Stricter association
        pose_weight=0.8,         # Emphasize pose similarity
        bbox_weight=0.2,         # Reduce bbox importance
        min_track_length=5       # Require longer tracks
    )
    
    print("Custom tracker configured with:")
    print(f"  Max disappeared: {tracker.max_disappeared}")
    print(f"  Max distance: {tracker.max_distance}")
    print(f"  Pose weight: {tracker.pose_weight}")
    print(f"  Bbox weight: {tracker.bbox_weight}")

def track_analysis_example():
    """Track analysis example"""
    print("\n=== Track Analysis Example ===")
    
    tracker = FlyTracker()
    
    # Simulate processing some frames
    for i in range(10):
        # Create dummy detections
        detections = []
        tracks = tracker.update(detections)
    
    # Analyze track statistics
    active_tracks = [t for t in tracker.tracks.values() if t.is_active]
    
    print(f"Total tracks: {len(tracker.tracks)}")
    print(f"Active tracks: {len(active_tracks)}")
    
    if active_tracks:
        lengths = [t.length for t in active_tracks]
        print(f"Average length: {np.mean(lengths):.2f}")
        print(f"Max length: {max(lengths)}")
        print(f"Min length: {min(lengths)}")

if __name__ == "__main__":
    basic_tracking_example()
    advanced_configuration_example()
    track_analysis_example()


