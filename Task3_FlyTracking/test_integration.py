#!/usr/bin/env python3
"""
Test script to verify Task 3 integration with Task 2's best model
"""

import os
import sys
from pathlib import Path

def test_model_availability():
    """Test if the best model from Task 2 is available"""
    print("Testing model availability...")
    
    model_paths = [
        "/mnt/storage5/Fruitfly/Task2_ModelTraining/results/yolo11m_training/weights/best.pt",
        "/mnt/storage5/Fruitfly/Task2_ModelTraining/results/yolo11s_training/weights/best.pt",
        "/mnt/storage5/Fruitfly/Task2_ModelTraining/results/yolo_training/weights/best.pt",
        "yolo11m-pose.pt"
    ]
    
    for path in model_paths:
        if os.path.exists(path):
            print(f"✓ Found model: {path}")
            return path
    
    print("✗ No trained models found!")
    return None

def test_image_data():
    """Test if image data is available"""
    print("\nTesting image data availability...")
    
    image_dirs = [
        "/mnt/storage5/Fruitfly/Extracted_Frames_task",
        "Extracted_Frames_task"
    ]
    
    for dir_path in image_dirs:
        if os.path.exists(dir_path):
            image_files = list(Path(dir_path).glob("*.jpg")) + list(Path(dir_path).glob("*.png"))
            if image_files:
                print(f"✓ Found {len(image_files)} images in: {dir_path}")
                return dir_path
    
    print("✗ No image data found!")
    return None

def test_integration():
    """Test the integrated pose estimation + tracking"""
    print("\nTesting integration...")
    
    try:
        from scripts.run_pose_estimation_and_tracking import PoseEstimator
        
        # Test model loading
        model_path = test_model_availability()
        if not model_path:
            return False
        
        # Test pose estimator initialization
        print("Testing pose estimator initialization...")
        estimator = PoseEstimator(model_path)
        print("✓ Pose estimator initialized successfully!")
        
        return True
        
    except Exception as e:
        print(f"✗ Integration test failed: {e}")
        return False

def main():
    print("="*60)
    print("TASK 3 INTEGRATION TEST")
    print("="*60)
    
    # Test model availability
    model_ok = test_model_availability() is not None
    
    # Test image data
    data_ok = test_image_data() is not None
    
    # Test integration
    integration_ok = test_integration()
    
    print("\n" + "="*60)
    print("TEST RESULTS")
    print("="*60)
    print(f"Model availability: {'✓ PASS' if model_ok else '✗ FAIL'}")
    print(f"Image data: {'✓ PASS' if data_ok else '✗ FAIL'}")
    print(f"Integration: {'✓ PASS' if integration_ok else '✗ FAIL'}")
    
    if model_ok and data_ok and integration_ok:
        print("\n🎉 All tests passed! Task 3 is ready to use with Task 2's best model.")
        return 0
    else:
        print("\n❌ Some tests failed. Please check the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
