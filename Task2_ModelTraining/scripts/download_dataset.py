#!/usr/bin/env python3
"""
Download and setup Roboflow dataset for Task 2
"""

import os
import subprocess
import zipfile
from pathlib import Path

def download_roboflow_dataset():
    """Download and extract Roboflow dataset"""
    print("Downloading Roboflow dataset...")
    
    # Download dataset
    cmd = 'curl -L "https://app.roboflow.com/ds/Rq0Cf3Q118?key=uaLNtFTi3V" > roboflow.zip'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error downloading dataset: {result.stderr}")
        return False
    
    print("Dataset downloaded successfully!")
    
    # Extract dataset
    print("Extracting dataset...")
    with zipfile.ZipFile('roboflow.zip', 'r') as zip_ref:
        zip_ref.extractall('.')
    
    # Remove zip file
    os.remove('roboflow.zip')
    print("Dataset extracted successfully!")
    
    # Check contents
    dataset_dirs = [d for d in os.listdir('.') if os.path.isdir(d) and 'Fruit' in d]
    if dataset_dirs:
        dataset_dir = dataset_dirs[0]
        print(f"Dataset directory: {dataset_dir}")
        
        # Check for data.yaml
        data_yaml = os.path.join(dataset_dir, 'data.yaml')
        if os.path.exists(data_yaml):
            print(f"Found data.yaml: {data_yaml}")
            return True
        else:
            print("Warning: data.yaml not found")
            return False
    else:
        print("Error: Dataset directory not found")
        return False

if __name__ == "__main__":
    success = download_roboflow_dataset()
    if success:
        print("Dataset setup complete!")
    else:
        print("Dataset setup failed!")

