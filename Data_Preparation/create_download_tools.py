#!/usr/bin/env python3
"""
Create download tools for video data transfer
"""

import os
from pathlib import Path

def create_windows_script():
    """Create Windows batch script"""
    script_content = """@echo off
echo Preparing video data for transfer...
set "SOURCE_DIR=C:\\Users\\siriy\\Kennesaw State University\\Dal Hyung Kim - 2023 FlyVialImage_Data"
set "TEMP_DIR=C:\\temp\\fly_video_data"
if not exist "%TEMP_DIR%" mkdir "%TEMP_DIR%"
echo Copying video files...
for %%f in ("%SOURCE_DIR%\\*.mp4") do copy "%%f" "%TEMP_DIR%\\"
for %%f in ("%SOURCE_DIR%\\*.avi") do copy "%%f" "%TEMP_DIR%\\"
for %%f in ("%SOURCE_DIR%\\*.mov") do copy "%%f" "%TEMP_DIR%\\"
echo Video files prepared in: %TEMP_DIR%
echo Next: Compress and upload to server
pause
"""
    
    script_path = Path("/mnt/storage5/Fruitfly/Data_Preparation/prepare_windows_data.bat")
    with open(script_path, 'w') as f:
        f.write(script_content)
    print(f"Created: {script_path}")
    return script_path

def create_download_guide():
    """Create download guide"""
    guide_content = """# Video Data Download Guide

## Source Location
Windows: `C:\\Users\\siriy\\Kennesaw State University\\Dal Hyung Kim - 2023 FlyVialImage_Data`
Target: `/mnt/storage5/Fruitfly/Data_Preparation/raw_videos/`

## Method 1: Using SCP (Recommended)

### Step 1: On Windows Machine
```cmd
# Open Command Prompt as Administrator
cd "C:\\Users\\siriy\\Kennesaw State University"
tar -czf fly_video_data.tar.gz "Dal Hyung Kim - 2023 FlyVialImage_Data"
```

### Step 2: Transfer to Server
```bash
scp fly_video_data.tar.gz user@server:/mnt/storage5/Fruitfly/Data_Preparation/
```

### Step 3: Extract on Server
```bash
cd /mnt/storage5/Fruitfly/Data_Preparation/
tar -xzf fly_video_data.tar.gz
mv "Dal Hyung Kim - 2023 FlyVialImage_Data" raw_videos/
```

## Method 2: Using rsync

```bash
rsync -avz --progress --include="*.mp4" --include="*.avi" --include="*.mov" --exclude="*" \\
  "C:/Users/siriy/Kennesaw State University/Dal Hyung Kim - 2023 FlyVialImage_Data/" \\
  user@server:/mnt/storage5/Fruitfly/Data_Preparation/raw_videos/
```

## Method 3: Manual Upload

1. Run `prepare_windows_data.bat` on Windows
2. Compress: `tar -czf fly_video_data.tar.gz -C C:\\temp fly_video_data`
3. Upload via cloud storage or USB
4. Extract on server

## Verification

```bash
# Check downloaded files
ls -la /mnt/storage5/Fruitfly/Data_Preparation/raw_videos/
find /mnt/storage5/Fruitfly/Data_Preparation/raw_videos/ -name "*.mp4" -o -name "*.avi" -o -name "*.mov"
```
"""
    
    guide_path = Path("/mnt/storage5/Fruitfly/Data_Preparation/DOWNLOAD_GUIDE.md")
    with open(guide_path, 'w') as f:
        f.write(guide_content)
    print(f"Created: {guide_path}")
    return guide_path

def create_validation_script():
    """Create validation script"""
    script_content = """#!/usr/bin/env python3
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
    
    print(f"\\nValidation complete: {valid_count}/{len(video_files)} files valid")
    return valid_count == len(video_files)

if __name__ == "__main__":
    import sys
    data_dir = sys.argv[1] if len(sys.argv) > 1 else "/mnt/storage5/Fruitfly/Data_Preparation/raw_videos"
    validate_videos(data_dir)
"""
    
    script_path = Path("/mnt/storage5/Fruitfly/Data_Preparation/validate_video_data.py")
    with open(script_path, 'w') as f:
        f.write(script_content)
    os.chmod(script_path, 0o755)
    print(f"Created: {script_path}")
    return script_path

def create_transfer_commands():
    """Create transfer commands file"""
    commands = """# Video Data Transfer Commands

## SCP Method (Recommended)
# On Windows:
cd "C:\\Users\\siriy\\Kennesaw State University"
tar -czf fly_video_data.tar.gz "Dal Hyung Kim - 2023 FlyVialImage_Data"

# Transfer:
scp fly_video_data.tar.gz user@server:/mnt/storage5/Fruitfly/Data_Preparation/

# On Server:
cd /mnt/storage5/Fruitfly/Data_Preparation/
tar -xzf fly_video_data.tar.gz
mv "Dal Hyung Kim - 2023 FlyVialImage_Data" raw_videos/

## rsync Method
rsync -avz --progress --include="*.mp4" --include="*.avi" --include="*.mov" --exclude="*" \\
  "C:/Users/siriy/Kennesaw State University/Dal Hyung Kim - 2023 FlyVialImage_Data/" \\
  user@server:/mnt/storage5/Fruitfly/Data_Preparation/raw_videos/

## Manual Method
1. Run prepare_windows_data.bat on Windows
2. Compress: tar -czf fly_video_data.tar.gz -C C:\\temp fly_video_data
3. Upload via cloud storage/USB
4. Extract on server
"""
    
    commands_path = Path("/mnt/storage5/Fruitfly/Data_Preparation/transfer_commands.txt")
    with open(commands_path, 'w') as f:
        f.write(commands)
    print(f"Created: {commands_path}")
    return commands_path

def main():
    """Main function"""
    print("Creating video data download tools...")
    print("=" * 50)
    
    # Create directories
    output_dir = Path("/mnt/storage5/Fruitfly/Data_Preparation")
    output_dir.mkdir(exist_ok=True)
    (output_dir / "raw_videos").mkdir(exist_ok=True)
    
    print(f"Output directory: {output_dir}")
    print()
    
    # Create tools
    create_windows_script()
    create_download_guide()
    create_validation_script()
    create_transfer_commands()
    
    print("\n" + "=" * 50)
    print("DOWNLOAD TOOLS CREATED SUCCESSFULLY!")
    print("=" * 50)
    print()
    print("Files created:")
    print("  - prepare_windows_data.bat (Windows script)")
    print("  - DOWNLOAD_GUIDE.md (Detailed instructions)")
    print("  - validate_video_data.py (Validation script)")
    print("  - transfer_commands.txt (Command reference)")
    print()
    print("Next steps:")
    print("1. Copy prepare_windows_data.bat to your Windows machine")
    print("2. Run it to prepare the video data")
    print("3. Use one of the transfer methods in DOWNLOAD_GUIDE.md")
    print("4. Run validation script to verify the data")

if __name__ == "__main__":
    main()
