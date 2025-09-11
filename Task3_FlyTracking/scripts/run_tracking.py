#!/usr/bin/env python3
"""
Main tracking script for Task 3
Usage: python run_tracking.py --data_dir <path> --output_dir <path>
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fly_tracker import FlyTracker, parse_yolo_pose_label
import argparse
from pathlib import Path
import json

def main():
    parser = argparse.ArgumentParser(description='Run fly tracking on pose detection results')
    parser.add_argument('--data_dir', required=True, help='Directory containing YOLO pose labels')
    parser.add_argument('--output_dir', required=True, help='Output directory for results')
    parser.add_argument('--max_disappeared', type=int, default=10, help='Max frames to maintain missing track')
    parser.add_argument('--max_distance', type=float, default=0.1, help='Max distance for association')
    parser.add_argument('--pose_weight', type=float, default=0.7, help='Weight for pose similarity')
    parser.add_argument('--bbox_weight', type=float, default=0.3, help='Weight for bbox similarity')
    
    args = parser.parse_args()
    
    # Create output directory
    Path(args.output_dir).mkdir(parents=True, exist_ok=True)
    
    # Initialize tracker
    tracker = FlyTracker(
        max_disappeared=args.max_disappeared,
        max_distance=args.max_distance,
        pose_weight=args.pose_weight,
        bbox_weight=args.bbox_weight
    )
    
    # Process all label files
    label_files = sorted(Path(args.data_dir).glob('*.txt'))
    print(f"Processing {len(label_files)} label files...")
    
    for i, label_file in enumerate(label_files):
        frame_id = label_file.stem
        detections = parse_yolo_pose_label(str(label_file), frame_id)
        tracks = tracker.update(detections)
        
        if (i + 1) % 100 == 0:
            print(f"Processed {i + 1}/{len(label_files)} frames")
    
    # Save results
    tracker.save_results(args.output_dir)
    print(f"Tracking complete! Results saved to {args.output_dir}")

if __name__ == "__main__":
    main()


