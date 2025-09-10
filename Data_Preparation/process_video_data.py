#!/usr/bin/env python3
"""
Video Data Processing Pipeline
Processes video files for pose estimation and tracking
"""

import os
import cv2
import numpy as np
from pathlib import Path
import json
from datetime import datetime
import argparse

def find_video_files(data_dir):
    """Find all video files in the data directory"""
    data_path = Path(data_dir)
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.webm']
    video_files = []
    
    for ext in video_extensions:
        video_files.extend(data_path.glob(f"**/*{ext}"))
    
    return sorted(video_files)

def get_video_info(video_path):
    """Get video information"""
    cap = cv2.VideoCapture(str(video_path))
    
    if not cap.isOpened():
        return None
    
    info = {
        'file': str(video_path),
        'name': video_path.name,
        'frames': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
        'fps': cap.get(cv2.CAP_PROP_FPS),
        'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        'duration': 0
    }
    
    if info['fps'] > 0:
        info['duration'] = info['frames'] / info['fps']
    
    cap.release()
    return info

def extract_frames_from_video(video_path, output_dir, frame_interval=30, max_frames=100):
    """Extract frames from video at specified intervals"""
    video_path = Path(video_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    cap = cv2.VideoCapture(str(video_path))
    
    if not cap.isOpened():
        print(f"ERROR: Cannot open {video_path}")
        return []
    
    frame_count = 0
    extracted_count = 0
    extracted_frames = []
    
    print(f"Extracting frames from {video_path.name}...")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        if frame_count % frame_interval == 0 and extracted_count < max_frames:
            # Create output filename
            frame_filename = f"{video_path.stem}_frame_{frame_count:06d}.jpg"
            frame_path = output_dir / frame_filename
            
            # Save frame
            cv2.imwrite(str(frame_path), frame)
            extracted_frames.append(str(frame_path))
            extracted_count += 1
            
            if extracted_count % 10 == 0:
                print(f"  Extracted {extracted_count} frames...")
        
        frame_count += 1
    
    cap.release()
    print(f"  Total: {extracted_count} frames extracted")
    return extracted_frames

def process_all_videos(video_dir, output_dir, frame_interval=30, max_frames_per_video=50):
    """Process all videos and extract frames"""
    video_dir = Path(video_dir)
    output_dir = Path(output_dir)
    
    # Create output directories
    frames_dir = output_dir / "extracted_frames"
    frames_dir.mkdir(parents=True, exist_ok=True)
    
    # Find all video files
    video_files = find_video_files(video_dir)
    print(f"Found {len(video_files)} video files")
    
    if not video_files:
        print("No video files found!")
        return
    
    # Process each video
    all_frames = []
    video_info = []
    
    for i, video_file in enumerate(video_files):
        print(f"\nProcessing video {i+1}/{len(video_files)}: {video_file.name}")
        
        # Get video info
        info = get_video_info(video_file)
        if info is None:
            print(f"  ERROR: Cannot read video {video_file.name}")
            continue
        
        video_info.append(info)
        print(f"  Info: {info['frames']} frames, {info['fps']:.1f} FPS, {info['width']}x{info['height']}")
        
        # Extract frames
        frames = extract_frames_from_video(
            video_file, 
            frames_dir, 
            frame_interval=frame_interval,
            max_frames=max_frames_per_video
        )
        
        all_frames.extend(frames)
        print(f"  Extracted {len(frames)} frames")
    
    # Save processing report
    report = {
        'timestamp': datetime.now().isoformat(),
        'total_videos': len(video_files),
        'processed_videos': len(video_info),
        'total_frames_extracted': len(all_frames),
        'frame_interval': frame_interval,
        'max_frames_per_video': max_frames_per_video,
        'video_info': video_info,
        'extracted_frames': all_frames
    }
    
    report_path = output_dir / "processing_report.json"
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n" + "="*60)
    print("VIDEO PROCESSING COMPLETE!")
    print("="*60)
    print(f"Total videos processed: {len(video_info)}")
    print(f"Total frames extracted: {len(all_frames)}")
    print(f"Frames saved to: {frames_dir}")
    print(f"Report saved to: {report_path}")
    
    return report

def validate_video_data(video_dir):
    """Validate all video files"""
    video_files = find_video_files(video_dir)
    
    if not video_files:
        print("No video files found!")
        return False
    
    print(f"Validating {len(video_files)} video files...")
    
    valid_count = 0
    total_duration = 0
    total_frames = 0
    
    for video_file in video_files:
        info = get_video_info(video_file)
        if info and info['frames'] > 0 and info['fps'] > 0:
            valid_count += 1
            total_duration += info['duration']
            total_frames += info['frames']
            print(f"✓ {video_file.name}: {info['frames']} frames, {info['duration']:.1f}s")
        else:
            print(f"✗ {video_file.name}: Invalid or corrupted")
    
    print(f"\nValidation Results:")
    print(f"Valid videos: {valid_count}/{len(video_files)}")
    print(f"Total duration: {total_duration/60:.1f} minutes")
    print(f"Total frames: {total_frames:,}")
    
    return valid_count == len(video_files)

def create_data_summary(video_dir, output_dir):
    """Create a summary of the video data"""
    video_files = find_video_files(video_dir)
    
    if not video_files:
        print("No video files found!")
        return
    
    # Analyze video files
    video_info = []
    for video_file in video_files:
        info = get_video_info(video_file)
        if info:
            video_info.append(info)
    
    # Create summary
    summary = {
        'total_videos': len(video_files),
        'valid_videos': len(video_info),
        'total_duration_minutes': sum(info['duration'] for info in video_info) / 60,
        'total_frames': sum(info['frames'] for info in video_info),
        'resolution_distribution': {},
        'fps_distribution': {},
        'duration_distribution': {},
        'file_size_distribution': {}
    }
    
    # Analyze distributions
    for info in video_info:
        res = f"{info['width']}x{info['height']}"
        summary['resolution_distribution'][res] = summary['resolution_distribution'].get(res, 0) + 1
        
        fps = round(info['fps'])
        summary['fps_distribution'][fps] = summary['fps_distribution'].get(fps, 0) + 1
        
        duration_min = round(info['duration'] / 60)
        summary['duration_distribution'][f"{duration_min}min"] = summary['duration_distribution'].get(f"{duration_min}min", 0) + 1
    
    # Save summary
    summary_path = Path(output_dir) / "data_summary.json"
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"Data summary saved to: {summary_path}")
    return summary

def main():
    parser = argparse.ArgumentParser(description='Process video data for pose estimation')
    parser.add_argument('--video_dir', type=str, 
                       default='/mnt/storage5/Fruitfly/Data_Preparation/FlyData',
                       help='Directory containing video files')
    parser.add_argument('--output_dir', type=str,
                       default='/mnt/storage5/Fruitfly/Data_Preparation',
                       help='Output directory for processed data')
    parser.add_argument('--frame_interval', type=int, default=30,
                       help='Extract every Nth frame')
    parser.add_argument('--max_frames', type=int, default=50,
                       help='Maximum frames per video')
    parser.add_argument('--validate_only', action='store_true',
                       help='Only validate videos, do not extract frames')
    parser.add_argument('--summary_only', action='store_true',
                       help='Only create data summary')
    
    args = parser.parse_args()
    
    print("Video Data Processing Pipeline")
    print("=" * 50)
    print(f"Video directory: {args.video_dir}")
    print(f"Output directory: {args.output_dir}")
    print(f"Frame interval: {args.frame_interval}")
    print(f"Max frames per video: {args.max_frames}")
    print()
    
    # Validate videos
    print("Step 1: Validating video files...")
    validation_success = validate_video_data(args.video_dir)
    
    if not validation_success:
        print("WARNING: Some video files are invalid!")
    
    if args.validate_only:
        return
    
    # Create data summary
    print("\nStep 2: Creating data summary...")
    summary = create_data_summary(args.video_dir, args.output_dir)
    
    if args.summary_only:
        return
    
    # Process videos
    print("\nStep 3: Processing videos and extracting frames...")
    report = process_all_videos(
        args.video_dir, 
        args.output_dir,
        frame_interval=args.frame_interval,
        max_frames_per_video=args.max_frames
    )
    
    print("\nProcessing complete! Next steps:")
    print("1. Review extracted frames in Data_Preparation/extracted_frames/")
    print("2. Run pose estimation on the extracted frames")
    print("3. Use the tracking pipeline on the results")

if __name__ == "__main__":
    main()
