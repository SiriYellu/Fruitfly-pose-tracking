#!/usr/bin/env python3
"""
Model Validation Script - Visual Inspection on New Video Data
Uses the best trained YOLO11m-pose model to validate on video frames
"""

import cv2
import os
import numpy as np
from ultralytics import YOLO
import matplotlib.pyplot as plt
from pathlib import Path

def extract_frames_from_video(video_path, output_dir, num_frames=5):
    """Extract random frames from video for validation"""
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"Error: Could not open video {video_path}")
        return []
    
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    duration = total_frames / fps
    
    print(f"Video: {os.path.basename(video_path)}")
    print(f"Total frames: {total_frames}, FPS: {fps:.2f}, Duration: {duration:.2f}s")
    
    # Extract random frames
    frame_indices = np.linspace(total_frames * 0.1, total_frames * 0.9, num_frames, dtype=int)
    extracted_frames = []
    
    for i, frame_idx in enumerate(frame_indices):
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()
        
        if ret:
            frame_path = os.path.join(output_dir, f"frame_{i+1:02d}_{frame_idx:06d}.jpg")
            cv2.imwrite(frame_path, frame)
            extracted_frames.append(frame_path)
            print(f"Extracted frame {i+1}: {frame_path}")
    
    cap.release()
    return extracted_frames

def run_pose_estimation(model_path, frame_paths, output_dir):
    """Run pose estimation on extracted frames with clean labels and scores"""
    print(f"\nLoading model: {model_path}")
    model = YOLO(model_path)
    
    results = []
    for frame_path in frame_paths:
        print(f"Processing: {os.path.basename(frame_path)}")
        
        # Run inference
        result = model(frame_path, conf=0.5, save=False, verbose=False)
        
        # Save visualization with custom annotations
        frame_name = os.path.splitext(os.path.basename(frame_path))[0]
        output_path = os.path.join(output_dir, f"{frame_name}_pose_result.jpg")
        
        # Create custom visualization with labels and scores
        annotated_frame = create_custom_visualization(result[0], frame_path)
        cv2.imwrite(output_path, annotated_frame)
        
        # Get detection info
        detections = result[0].boxes
        keypoints = result[0].keypoints
        
        num_detections = len(detections) if detections is not None else 0
        num_keypoints = len(keypoints) if keypoints is not None else 0
        
        # Calculate average confidence
        avg_conf = 0
        if detections is not None and len(detections) > 0:
            avg_conf = float(detections.conf.mean())
        
        print(f"  Detections: {num_detections}, Keypoints: {num_keypoints}, Avg Conf: {avg_conf:.3f}")
        
        results.append({
            'frame': frame_path,
            'output': output_path,
            'detections': num_detections,
            'keypoints': num_keypoints,
            'avg_confidence': avg_conf
        })
    
    return results

def create_custom_visualization(result, frame_path):
    """Create custom visualization with clean labels and scores"""
    # Load original image
    img = cv2.imread(frame_path)
    img_height, img_width = img.shape[:2]
    
    # Get detections and keypoints
    boxes = result.boxes
    keypoints = result.keypoints
    
    if boxes is None or keypoints is None:
        return img
    
    # Draw detections with clean labels
    for i, (box, kpts) in enumerate(zip(boxes, keypoints)):
        # Get box coordinates
        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
        conf = float(box.conf[0])
        
        # Draw bounding box (thin line)
        cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 1)
        
        # Draw keypoints
        if kpts is not None:
            kpts_data = kpts.data[0].cpu().numpy()
            for j, (x, y, v) in enumerate(kpts_data):
                if v > 0.5:  # Only draw visible keypoints
                    # Color coding: Head=Green, Thorax=Blue, Abdomen=Red
                    colors = [(0, 255, 0), (255, 0, 0), (0, 0, 255)]
                    cv2.circle(img, (int(x), int(y)), 3, colors[j], -1)
                    
                    # Draw skeleton lines
                    if j < len(kpts_data) - 1:
                        next_x, next_y, next_v = kpts_data[j + 1]
                        if next_v > 0.5:
                            cv2.line(img, (int(x), int(y)), (int(next_x), int(next_y)), (255, 255, 255), 1)
        
        # Add clean label with score (top-left corner)
        label = f"Fly {i+1}: {conf:.2f}"
        label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.4, 1)[0]
        
        # Background rectangle for label
        cv2.rectangle(img, (int(x1), int(y1) - label_size[1] - 4), 
                     (int(x1) + label_size[0] + 4, int(y1)), (0, 0, 0), -1)
        
        # Label text
        cv2.putText(img, label, (int(x1) + 2, int(y1) - 2), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
    
    # Add frame summary (top-right corner)
    summary_text = f"Flies: {len(boxes)} | Avg Conf: {float(boxes.conf.mean()):.2f}"
    summary_size = cv2.getTextSize(summary_text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
    
    # Background for summary
    cv2.rectangle(img, (img_width - summary_size[0] - 10, 10), 
                 (img_width - 5, summary_size[1] + 15), (0, 0, 0), -1)
    
    # Summary text
    cv2.putText(img, summary_text, (img_width - summary_size[0] - 5, summary_size[1] + 10), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    return img

def find_random_videos(base_path, num_videos=5):
    """Find random video files from the dataset"""
    import glob
    import random
    
    # Search for video files in all subdirectories
    video_extensions = ['*.mp4', '*.mov', '*.avi', '*.mkv']
    all_videos = []
    
    for ext in video_extensions:
        pattern = os.path.join(base_path, '**', ext)
        videos = glob.glob(pattern, recursive=True)
        all_videos.extend(videos)
    
    # Remove duplicates and select random subset
    all_videos = list(set(all_videos))
    random.shuffle(all_videos)
    
    return all_videos[:num_videos]

def main():
    # Paths
    video_base_path = "/mnt/storage5/Fruitfly/Task1_PoseEstimation/Task1/Data_Preparation/raw_videos"
    model_path = "/mnt/storage5/Fruitfly/Task1_PoseEstimation/Task2_ModelTraining/results/yolo11m_training/weights/best.pt"
    
    # Create output directories
    validation_dir = "/mnt/storage5/Fruitfly/Task1_PoseEstimation/validation_results"
    frames_dir = os.path.join(validation_dir, "extracted_frames")
    results_dir = os.path.join(validation_dir, "pose_results")
    
    os.makedirs(frames_dir, exist_ok=True)
    os.makedirs(results_dir, exist_ok=True)
    
    print("=" * 60)
    print("MODEL VALIDATION - VISUAL INSPECTION ON 5 RANDOM VIDEOS")
    print("=" * 60)
    
    # Check if model exists
    if not os.path.exists(model_path):
        print(f"Error: Model not found at {model_path}")
        return
    
    # Find random videos
    print("\n1. FINDING RANDOM VIDEOS")
    print("-" * 40)
    video_paths = find_random_videos(video_base_path, num_videos=5)
    
    if not video_paths:
        print(f"No videos found in {video_base_path}")
        return
    
    print(f"Found {len(video_paths)} videos:")
    for i, video_path in enumerate(video_paths, 1):
        print(f"  {i}. {os.path.basename(video_path)}")
    
    # Process each video
    all_results = []
    for video_idx, video_path in enumerate(video_paths, 1):
        print(f"\n2.{video_idx} PROCESSING VIDEO: {os.path.basename(video_path)}")
        print("-" * 50)
        
        # Extract frames from video
        video_frames_dir = os.path.join(frames_dir, f"video_{video_idx}")
        os.makedirs(video_frames_dir, exist_ok=True)
        
        frame_paths = extract_frames_from_video(video_path, video_frames_dir, num_frames=5)
        
        if not frame_paths:
            print(f"No frames extracted from {os.path.basename(video_path)}")
            continue
        
        # Run pose estimation
        video_results_dir = os.path.join(results_dir, f"video_{video_idx}")
        os.makedirs(video_results_dir, exist_ok=True)
        
        results = run_pose_estimation(model_path, frame_paths, video_results_dir)
        all_results.extend(results)
    
    # Overall summary
    print("\n3. OVERALL VALIDATION SUMMARY")
    print("-" * 40)
    if all_results:
        total_detections = sum(r['detections'] for r in all_results)
        total_keypoints = sum(r['keypoints'] for r in all_results)
        avg_confidence = sum(r['avg_confidence'] for r in all_results) / len(all_results)
        
        print(f"Videos processed: {len(video_paths)}")
        print(f"Frames processed: {len(all_results)}")
        print(f"Total detections: {total_detections}")
        print(f"Total keypoints: {total_keypoints}")
        print(f"Average detections per frame: {total_detections/len(all_results):.1f}")
        print(f"Average keypoints per frame: {total_keypoints/len(all_results):.1f}")
        print(f"Average confidence score: {avg_confidence:.3f}")
        
        print(f"\nResults saved to: {validation_dir}")
        print(f"Extracted frames: {frames_dir}")
        print(f"Pose results: {results_dir}")
        
        # List output files with confidence scores
        print("\n4. OUTPUT FILES BY VIDEO")
        print("-" * 40)
        for video_idx, video_path in enumerate(video_paths, 1):
            print(f"\nVideo {video_idx}: {os.path.basename(video_path)}")
            video_results = [r for r in all_results if f"video_{video_idx}" in r['output']]
            for result in video_results:
                print(f"  Original: {os.path.basename(result['frame'])}")
                print(f"  Result:   {os.path.basename(result['output'])}")
                print(f"  Detections: {result['detections']}, Keypoints: {result['keypoints']}, Avg Conf: {result['avg_confidence']:.3f}")
    else:
        print("No results generated.")

if __name__ == "__main__":
    main()
