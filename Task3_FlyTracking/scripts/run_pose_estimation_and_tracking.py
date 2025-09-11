#!/usr/bin/env python3
"""
Updated Task 3: Pose Estimation + Fly Tracking Pipeline
Uses the best YOLO11m-pose model from Task 2 for pose estimation
Then runs multi-object tracking on the results
"""

import os
import sys
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
from ultralytics import YOLO

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fly_tracker import FlyTracker, Detection

class PoseEstimator:
    """Pose estimation using the best YOLO11m-pose model from Task 2"""
    
    def __init__(self, model_path: str = None):
        """Initialize pose estimator with best model"""
        if model_path is None:
            # Try to find the best model from Task 2
            possible_paths = [
                "/mnt/storage5/Fruitfly/Task2_ModelTraining/results/yolo11m_training/weights/best.pt",
                "/mnt/storage5/Fruitfly/Task2_ModelTraining/results/yolo11s_training/weights/best.pt",
                "/mnt/storage5/Fruitfly/Task2_ModelTraining/results/yolo_training/weights/best.pt",
                "yolo11m-pose.pt"
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    model_path = path
                    break
            
            if model_path is None:
                raise FileNotFoundError("No trained model found! Please ensure Task 2 is completed.")
        
        print(f"Loading pose estimation model: {model_path}")
        self.model = YOLO(model_path)
        print("✓ Model loaded successfully!")
    
    def estimate_poses(self, image_path: str, frame_id: str, conf_threshold: float = 0.25) -> List[Detection]:
        """Run pose estimation on a single image"""
        # Load image
        image = cv2.imread(image_path)
        if image is None:
            print(f"Warning: Could not load image {image_path}")
            return []
        
        # Run inference
        results = self.model(image, conf=conf_threshold)
        
        detections = []
        for result in results:
            if result.keypoints is not None and len(result.keypoints.data) > 0:
                for detection_keypoints in result.keypoints.data:
                    if detection_keypoints is not None and len(detection_keypoints) >= 3:
                        # Extract keypoints (x, y, visibility)
                        keypoints = []
                        for kpt in detection_keypoints:
                            if len(kpt) >= 3:
                                x, y, v = float(kpt[0]), float(kpt[1]), float(kpt[2])
                                # Normalize coordinates
                                x_norm = x / image.shape[1]
                                y_norm = y / image.shape[0]
                                keypoints.append((x_norm, y_norm, v))
                        
                        # Get bounding box from keypoints
                        if len(keypoints) >= 3:
                            # Calculate bounding box from keypoints
                            valid_points = [(x, y) for x, y, v in keypoints if v > 0.5]
                            if valid_points:
                                xs, ys = zip(*valid_points)
                                x_min, x_max = min(xs), max(xs)
                                y_min, y_max = min(ys), max(ys)
                                
                                # Add some padding
                                padding = 0.05
                                x_min = max(0, x_min - padding)
                                y_min = max(0, y_min - padding)
                                x_max = min(1, x_max + padding)
                                y_max = min(1, y_max + padding)
                                
                                # Convert to center, width, height format
                                x_center = (x_min + x_max) / 2
                                y_center = (y_min + y_max) / 2
                                width = x_max - x_min
                                height = y_max - y_min
                                
                                # Create detection
                                detection = Detection(
                                    frame_id=frame_id,
                                    bbox=(x_center, y_center, width, height),
                                    keypoints=keypoints,
                                    confidence=1.0  # YOLO confidence is already filtered
                                )
                                detections.append(detection)
        
        return detections

def process_video_sequence(image_dir: str, output_dir: str, model_path: str = None):
    """Process a sequence of images for pose estimation and tracking"""
    
    print("="*80)
    print("TASK 3: POSE ESTIMATION + FLY TRACKING")
    print("="*80)
    
    # Initialize pose estimator
    pose_estimator = PoseEstimator(model_path)
    
    # Initialize tracker
    tracker = FlyTracker(
        max_disappeared=10,
        max_distance=0.1,
        pose_weight=0.7,
        bbox_weight=0.3,
        min_track_length=3
    )
    
    # Get all image files
    image_files = sorted(Path(image_dir).glob("*.jpg")) + sorted(Path(image_dir).glob("*.png"))
    print(f"Found {len(image_files)} images to process")
    
    if not image_files:
        print("No images found in the directory!")
        return False
    
    # Process each image
    all_detections = []
    frame_stats = []
    
    for i, image_file in enumerate(image_files):
        frame_id = image_file.stem
        print(f"Processing frame {i+1}/{len(image_files)}: {frame_id}")
        
        # Run pose estimation
        detections = pose_estimator.estimate_poses(str(image_file), frame_id)
        all_detections.extend(detections)
        
        # Update tracker
        tracks = tracker.update(detections)
        
        # Record frame statistics
        frame_stats.append({
            'frame_id': frame_id,
            'num_detections': len(detections),
            'num_tracks': len([t for t in tracks if t.is_active]),
            'image_path': str(image_file)
        })
        
        if (i + 1) % 50 == 0:
            print(f"  Processed {i + 1}/{len(image_files)} frames")
            print(f"  Current active tracks: {len([t for t in tracks if t.is_active])}")
    
    print(f"\n✓ Pose estimation complete!")
    print(f"  Total detections: {len(all_detections)}")
    print(f"  Total tracks: {len(tracker.tracks)}")
    print(f"  Active tracks: {len([t for t in tracker.tracks.values() if t.is_active])}")
    
    # Save results
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Save tracking results
    tracker.save_results(str(output_path / "tracking_results"))
    
    # Save frame statistics
    frame_df = pd.DataFrame(frame_stats)
    frame_df.to_csv(output_path / "tracking_results" / "frames_summary.csv", index=False)
    
    # Save pose estimation results
    pose_results = {
        'total_frames': len(image_files),
        'total_detections': len(all_detections),
        'model_used': str(pose_estimator.model.ckpt_path),
        'processing_timestamp': datetime.now().isoformat()
    }
    
    with open(output_path / "tracking_results" / "pose_estimation_stats.json", 'w') as f:
        json.dump(pose_results, f, indent=2)
    
    print(f"\n✓ Results saved to: {output_path}")
    return True

def main():
    parser = argparse.ArgumentParser(description='Run pose estimation and fly tracking')
    parser.add_argument('--image_dir', required=True, 
                       help='Directory containing input images')
    parser.add_argument('--output_dir', required=True, 
                       help='Output directory for results')
    parser.add_argument('--model_path', type=str, default=None,
                       help='Path to YOLO model (default: auto-detect best model)')
    parser.add_argument('--conf_threshold', type=float, default=0.25,
                       help='Confidence threshold for detections')
    
    args = parser.parse_args()
    
    # Check if image directory exists
    if not Path(args.image_dir).exists():
        print(f"Error: Image directory not found: {args.image_dir}")
        return 1
    
    # Process the video sequence
    success = process_video_sequence(
        args.image_dir, 
        args.output_dir, 
        args.model_path
    )
    
    if success:
        print("\n🎉 Task 3 completed successfully!")
        print(f"Results saved to: {args.output_dir}")
        return 0
    else:
        print("\n❌ Task 3 failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
