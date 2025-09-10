#!/usr/bin/env python3
"""
Setup script for video data download tools
Creates all necessary scripts and guides for downloading video data
"""

import os
import subprocess
from pathlib import Path

def check_rsync_available():
    """Check if rsync is available on the system"""
    try:
        subprocess.run(['rsync', '--version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def check_scp_available():
    """Check if scp is available on the system"""
    try:
        subprocess.run(['scp'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def create_windows_script():
    """Create a Windows batch script to help with data transfer"""
    windows_script = """@echo off
REM Windows script to prepare video data for transfer
REM Run this script on Windows machine with the video data

echo Preparing video data for transfer...

REM Set source directory
set "SOURCE_DIR=C:\\Users\\siriy\\Kennesaw State University\\Dal Hyung Kim - 2023 FlyVialImage_Data"
set "TEMP_DIR=C:\\temp\\fly_video_data"

REM Create temporary directory
if not exist "%TEMP_DIR%" mkdir "%TEMP_DIR%"

REM Copy video files to temporary directory
echo Copying video files...
for %%f in ("%SOURCE_DIR%\\*.mp4") do copy "%%f" "%TEMP_DIR%\\"
for %%f in ("%SOURCE_DIR%\\*.avi") do copy "%%f" "%TEMP_DIR%\\"
for %%f in ("%SOURCE_DIR%\\*.mov") do copy "%%f" "%TEMP_DIR%\\"

REM Create file list
echo Creating file list...
dir /b "%TEMP_DIR%\\*.mp4" "%TEMP_DIR%\\*.avi" "%TEMP_DIR%\\*.mov" > "%TEMP_DIR%\\file_list.txt"

echo.
echo Video files prepared in: %TEMP_DIR%
echo File list created: %TEMP_DIR%\\file_list.txt
echo.
echo Next steps:
echo 1. Compress the folder: tar -czf fly_video_data.tar.gz -C C:\\temp fly_video_data
echo 2. Upload to server using SCP or SFTP
echo 3. Or use rsync if available
echo.
pause
"""
    
    script_path = Path("/mnt/storage5/Fruitfly/Data_Preparation/prepare_windows_data.bat")
    with open(script_path, 'w') as f:
        f.write(windows_script)
    
    print(f"Windows script created: {script_path}")
    return script_path

def create_rsync_commands():
    """Create rsync commands for data transfer"""
    commands = {
        'from_windows': """
# On Windows machine (if rsync is available):
# Install rsync for Windows (e.g., via WSL or Cygwin)

# Basic rsync command:
rsync -avz --progress "C:/Users/siriy/Kennesaw State University/Dal Hyung Kim - 2023 FlyVialImage_Data/" user@server:/mnt/storage5/Fruitfly/Data_Preparation/raw_videos/

# With specific file types:
rsync -avz --progress --include="*.mp4" --include="*.avi" --include="*.mov" --exclude="*" "C:/Users/siriy/Kennesaw State University/Dal Hyung Kim - 2023 FlyVialImage_Data/" user@server:/mnt/storage5/Fruitfly/Data_Preparation/raw_videos/
""",
        'from_linux': """
# On Linux server (if you have access to Windows share):
# Mount Windows share first
sudo mkdir -p /mnt/windows_share
sudo mount -t cifs //windows-machine-ip/Users /mnt/windows_share -o username=siriy,uid=1000,gid=1000

# Then copy files
rsync -avz --progress /mnt/windows_share/siriy/Kennesaw\\ State\\ University/Dal\\ Hyung\\ Kim\\ -\\ 2023\\ FlyVialImage_Data/ /mnt/storage5/Fruitfly/Data_Preparation/raw_videos/
"""
    }
    
    return commands

def create_scp_commands():
    """Create SCP commands for data transfer"""
    commands = {
        'compress_and_transfer': """
# On Windows machine:
# 1. Compress the data
tar -czf fly_video_data.tar.gz -C "C:/Users/siriy/Kennesaw State University" "Dal Hyung Kim - 2023 FlyVialImage_Data"

# 2. Transfer to server
scp fly_video_data.tar.gz user@server:/mnt/storage5/Fruitfly/Data_Preparation/

# On Linux server:
# 3. Extract the data
cd /mnt/storage5/Fruitfly/Data_Preparation/
tar -xzf fly_video_data.tar.gz
mv "Dal Hyung Kim - 2023 FlyVialImage_Data" raw_videos/
""",
        'direct_transfer': """
# Transfer files directly (if network is fast enough)
scp -r "C:/Users/siriy/Kennesaw State University/Dal Hyung Kim - 2023 FlyVialImage_Data/*" user@server:/mnt/storage5/Fruitfly/Data_Preparation/raw_videos/
"""
    }
    
    return commands

def create_sftp_script():
    """Create SFTP script for data transfer"""
    sftp_script = """# SFTP script for transferring video data
# Run with: sftp -b sftp_script.txt user@server

# Connect to server
cd /mnt/storage5/Fruitfly/Data_Preparation/raw_videos/

# Create directory structure
mkdir -p raw_videos

# Upload files (run this from Windows machine)
put -r "C:/Users/siriy/Kennesaw State University/Dal Hyung Kim - 2023 FlyVialImage_Data/*" raw_videos/

# Exit
quit
"""
    
    script_path = Path("/mnt/storage5/Fruitfly/Data_Preparation/sftp_script.txt")
    with open(script_path, 'w') as f:
        f.write(sftp_script)
    
    print(f"SFTP script created: {script_path}")
    return script_path

def create_download_guide():
    """Create comprehensive download guide"""
    guide = """# Video Data Download Guide

## Overview
This guide helps you download video data from the Windows path to the Linux server.

## Source Location
- **Windows Path**: `C:\\Users\\siriy\\Kennesaw State University\\Dal Hyung Kim - 2023 FlyVialImage_Data`
- **Target Location**: `/mnt/storage5/Fruitfly/Data_Preparation/raw_videos/`

## Method 1: Using rsync (Recommended)

### Prerequisites
- rsync installed on Windows (via WSL, Cygwin, or Windows rsync)
- SSH access to the server

### Commands
```bash
# From Windows machine
rsync -avz --progress --include="*.mp4" --include="*.avi" --include="*.mov" --exclude="*" \\
  "C:/Users/siriy/Kennesaw State University/Dal Hyung Kim - 2023 FlyVialImage_Data/" \\
  user@server:/mnt/storage5/Fruitfly/Data_Preparation/raw_videos/
```

## Method 2: Using SCP

### Step 1: Compress on Windows
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

## Method 3: Using SFTP

### Step 1: Create SFTP Script
Use the generated `sftp_script.txt` file.

### Step 2: Run SFTP
```bash
sftp -b sftp_script.txt user@server
```

## Method 4: Manual Upload

### Step 1: Prepare Data on Windows
1. Run `prepare_windows_data.bat` on Windows machine
2. This will copy all video files to `C:\\temp\\fly_video_data\\`

### Step 2: Compress and Upload
1. Compress the folder: `tar -czf fly_video_data.tar.gz -C C:\\temp fly_video_data`
2. Upload using any file transfer method (cloud storage, USB, etc.)

### Step 3: Extract on Server
```bash
cd /mnt/storage5/Fruitfly/Data_Preparation/
tar -xzf fly_video_data.tar.gz
mv fly_video_data/* raw_videos/
```

## Verification

### Check Downloaded Files
```bash
# List all video files
find /mnt/storage5/Fruitfly/Data_Preparation/raw_videos/ -name "*.mp4" -o -name "*.avi" -o -name "*.mov" | wc -l

# Check file sizes
du -sh /mnt/storage5/Fruitfly/Data_Preparation/raw_videos/

# List file types
file /mnt/storage5/Fruitfly/Data_Preparation/raw_videos/*
```

### Expected File Structure
```
raw_videos/
├── video1.mp4
├── video2.avi
├── video3.mov
└── ...
```

## Troubleshooting

### Common Issues
1. **Permission Denied**: Check file permissions on Windows
2. **Network Timeout**: Use compression for large files
3. **Path Issues**: Use forward slashes in rsync commands
4. **Space Issues**: Check available disk space on server

### Solutions
1. **Run as Administrator** on Windows
2. **Use compression** for large datasets
3. **Transfer in batches** if files are very large
4. **Check network connection** stability

## Next Steps
After successful download:
1. Run data validation: `python validate_video_data.py`
2. Extract frames: `python extract_frames.py`
3. Begin pose estimation pipeline

## Support
If you encounter issues:
1. Check the troubleshooting section
2. Verify network connectivity
3. Ensure sufficient disk space
4. Contact system administrator if needed
"""
    
    guide_path = Path("/mnt/storage5/Fruitfly/Data_Preparation/DOWNLOAD_GUIDE.md")
    with open(guide_path, 'w') as f:
        f.write(guide)
    
    print(f"Download guide created: {guide_path}")
    return guide_path

def create_validation_script():
    """Create script to validate downloaded video data"""
    validation_script = """#!/usr/bin/env python3
'''
Video Data Validation Script
Validates downloaded video data for completeness and quality
'''

import os
import cv2
from pathlib import Path
import json
from datetime import datetime

def validate_video_files(data_dir):
    """Validate video files in the data directory"""
    data_path = Path(data_dir)
    
    if not data_path.exists():
        print(f"ERROR: Data directory not found: {data_dir}")
        return False
    
    # Find all video files
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.webm']
    video_files = []
    
    for ext in video_extensions:
        video_files.extend(data_path.glob(f"**/*{ext}"))
    
    if not video_files:
        print("ERROR: No video files found!")
        return False
    
    print(f"Found {len(video_files)} video files")
    
    # Validate each video file
    valid_files = []
    invalid_files = []
    
    for video_file in video_files:
        print(f"Validating: {video_file.name}")
        
        try:
            # Open video file
            cap = cv2.VideoCapture(str(video_file))
            
            if not cap.isOpened():
                print(f"  ERROR: Cannot open {video_file.name}")
                invalid_files.append(str(video_file))
                continue
            
            # Get video properties
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            duration = frame_count / fps if fps > 0 else 0
            
            # Check if video is valid
            if frame_count > 0 and fps > 0 and width > 0 and height > 0:
                valid_files.append({
                    'file': str(video_file),
                    'frames': frame_count,
                    'fps': fps,
                    'width': width,
                    'height': height,
                    'duration': duration
                })
                print(f"  ✓ Valid: {frame_count} frames, {fps:.1f} FPS, {width}x{height}")
            else:
                print(f"  ERROR: Invalid video properties")
                invalid_files.append(str(video_file))
            
            cap.release()
            
        except Exception as e:
            print(f"  ERROR: {e}")
            invalid_files.append(str(video_file))
    
    # Generate report
    report = {
        'timestamp': datetime.now().isoformat(),
        'total_files': len(video_files),
        'valid_files': len(valid_files),
        'invalid_files': len(invalid_files),
        'valid_file_list': valid_files,
        'invalid_file_list': invalid_files
    }
    
    # Save report
    report_path = data_path / 'validation_report.json'
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\\nValidation complete!")
    print(f"Valid files: {len(valid_files)}")
    print(f"Invalid files: {len(invalid_files)}")
    print(f"Report saved: {report_path}")
    
    return len(invalid_files) == 0

if __name__ == "__main__":
    import sys
    
    data_dir = sys.argv[1] if len(sys.argv) > 1 else "/mnt/storage5/Fruitfly/Data_Preparation/raw_videos"
    
    print("Video Data Validation")
    print("=" * 50)
    print(f"Data directory: {data_dir}")
    print()
    
    success = validate_video_files(data_dir)
    sys.exit(0 if success else 1)
"""
    
    script_path = Path("/mnt/storage5/Fruitfly/Data_Preparation/validate_video_data.py")
    with open(script_path, 'w') as f:
        f.write(validation_script)
    
    # Make it executable
    os.chmod(script_path, 0o755)
    
    print(f"Validation script created: {script_path}")
    return script_path

def main():
    """Main function to create download tools"""
    print("Creating video data download tools...")
    print("=" * 50)
    
    # Create output directory
    output_dir = Path("/mnt/storage5/Fruitfly/Data_Preparation")
    output_dir.mkdir(exist_ok=True)
    
    # Create raw_videos directory
    raw_videos_dir = output_dir / "raw_videos"
    raw_videos_dir.mkdir(exist_ok=True)
    
    print(f"Output directory: {output_dir}")
    print(f"Raw videos directory: {raw_videos_dir}")
    print()
    
    # Check available tools
    print("Checking available transfer tools...")
    rsync_available = check_rsync_available()
    scp_available = check_scp_available()
    
    print(f"rsync available: {rsync_available}")
    print(f"scp available: {scp_available}")
    print()
    
    # Create tools
    print("Creating download tools...")
    
    # 1. Windows preparation script
    windows_script = create_windows_script()
    
    # 2. SFTP script
    sftp_script = create_sftp_script()
    
    # 3. Download guide
    download_guide = create_download_guide()
    
    # 4. Validation script
    validation_script = create_validation_script()
    
    # 5. Transfer commands
    rsync_commands = create_rsync_commands()
    scp_commands = create_scp_commands()
    
    # Save transfer commands
    commands_file = output_dir / "transfer_commands.txt"
    with open(commands_file, 'w') as f:
        f.write("RSYNC COMMANDS\n")
        f.write("=" * 50 + "\n")
        f.write(rsync_commands['from_windows'])
        f.write("\n\n")
        f.write(rsync_commands['from_linux'])
        f.write("\n\n")
        f.write("SCP COMMANDS\n")
        f.write("=" * 50 + "\n")
        f.write(scp_commands['compress_and_transfer'])
        f.write("\n\n")
        f.write(scp_commands['direct_transfer'])
    
    print(f"Transfer commands saved: {commands_file}")
    
    print("\n" + "=" * 50)
    print("DOWNLOAD TOOLS CREATED SUCCESSFULLY!")
    print("=" * 50)
    print()
    print("Files created:")
    print(f"  - {windows_script}")
    print(f"  - {sftp_script}")
    print(f"  - {download_guide}")
    print(f"  - {validation_script}")
    print(f"  - {commands_file}")
    print()
    print("Next steps:")
    print("1. Copy the Windows script to your Windows machine")
    print("2. Run the Windows script to prepare the data")
    print("3. Use one of the transfer methods in the download guide")
    print("4. Run the validation script to verify the data")
    print()
    print("For detailed instructions, see: DOWNLOAD_GUIDE.md")

if __name__ == "__main__":
    main()
