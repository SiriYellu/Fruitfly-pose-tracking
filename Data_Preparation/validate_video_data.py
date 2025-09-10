#!/usr/bin/env python3
import os
import cv2
from pathlib import Path

def validate_videos(data_dir):
    data_path = Path(data_dir)
    if not data_path.exists():
        print(f"ERROR: Directory not found: {data_dir}")
        return False
    
    video_files = list(data_path.glob("**/*.mp4")) + list(data_path.glob("**/*.avi")) + list(data_path.glob("**/*.mov"))
    
    if not video_files:
        print("ERROR: No video files found!")
        return False
    
    print(f"Found {len(video_files)} video files")
    
    valid_count = 0
    for video_file in video_files:
        try:
            cap = cv2.VideoCapture(str(video_file))
            if cap.isOpened():
                frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                fps = cap.get(cv2.CAP_PROP_FPS)
                if frame_count > 0 and fps > 0:
                    print(f"✓ {video_file.name}: {frame_count} frames, {fps:.1f} FPS")
                    valid_count += 1
                else:
                    print(f"✗ {video_file.name}: Invalid properties")
            else:
                print(f"✗ {video_file.name}: Cannot open")
            cap.release()
        except Exception as e:
            print(f"✗ {video_file.name}: Error - {e}")
    
    print(f"\nValidation complete: {valid_count}/{len(video_files)} files valid")
    return valid_count == len(video_files)

if __name__ == "__main__":
    import sys
    data_dir = sys.argv[1] if len(sys.argv) > 1 else "/mnt/storage5/Fruitfly/Data_Preparation/raw_videos"
    validate_videos(data_dir)
