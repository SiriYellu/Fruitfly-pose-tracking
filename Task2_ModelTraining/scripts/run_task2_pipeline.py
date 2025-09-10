#!/usr/bin/env python3
"""
Complete Task 2 pipeline: Download dataset, train model, autolabel frames
"""

import os
import sys
import subprocess
from pathlib import Path

def run_step(step_name, script_path, *args):
    """Run a step in the pipeline"""
    print(f"\n{'='*60}")
    print(f"STEP: {step_name}")
    print(f"{'='*60}")
    
    cmd = [sys.executable, script_path] + list(args)
    print(f"Running: {' '.join(cmd)}")
    
    result = subprocess.run(cmd, cwd="Task2_ModelTraining")
    
    if result.returncode == 0:
        print(f"✅ {step_name} completed successfully!")
        return True
    else:
        print(f"❌ {step_name} failed!")
        return False

def main():
    """Run complete Task 2 pipeline"""
    print("🚀 Starting Task 2: Model Training Pipeline")
    print("=" * 60)
    
    # Change to Task2 directory
    os.chdir("Task2_ModelTraining")
    
    steps = [
        ("Download Dataset", "scripts/download_dataset.py"),
        ("Train YOLO Model", "scripts/train_yolo.py"),
        ("Auto-label Frames", "scripts/autolabel_frames.py")
    ]
    
    success_count = 0
    
    for step_name, script_path in steps:
        if run_step(step_name, script_path):
            success_count += 1
        else:
            print(f"\n❌ Pipeline stopped at: {step_name}")
            break
    
    print(f"\n{'='*60}")
    print(f"PIPELINE SUMMARY")
    print(f"{'='*60}")
    print(f"Steps completed: {success_count}/{len(steps)}")
    
    if success_count == len(steps):
        print("🎉 Task 2 pipeline completed successfully!")
        print("\nResults available in:")
        print("- Task2_ModelTraining/results/yolo_training/ (trained model)")
        print("- Task2_ModelTraining/results/autolabeled_frames/ (labeled images)")
        return True
    else:
        print("❌ Task 2 pipeline failed!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

