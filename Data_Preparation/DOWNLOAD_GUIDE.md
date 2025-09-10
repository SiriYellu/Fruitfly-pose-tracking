# Video Data Download Guide

## Source Location
Windows: `C:\Users\siriy\Kennesaw State University\Dal Hyung Kim - 2023 FlyVialImage_Data`
Target: `/mnt/storage5/Fruitfly/Data_Preparation/raw_videos/`

## Method 1: Using SCP (Recommended)

### Step 1: On Windows Machine
```cmd
# Open Command Prompt as Administrator
cd "C:\Users\siriy\Kennesaw State University"
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
rsync -avz --progress --include="*.mp4" --include="*.avi" --include="*.mov" --exclude="*" \
  "C:/Users/siriy/Kennesaw State University/Dal Hyung Kim - 2023 FlyVialImage_Data/" \
  user@server:/mnt/storage5/Fruitfly/Data_Preparation/raw_videos/
```

## Method 3: Manual Upload

1. Run `prepare_windows_data.bat` on Windows
2. Compress: `tar -czf fly_video_data.tar.gz -C C:\temp fly_video_data`
3. Upload via cloud storage or USB
4. Extract on server

## Verification

```bash
# Check downloaded files
ls -la /mnt/storage5/Fruitfly/Data_Preparation/raw_videos/
find /mnt/storage5/Fruitfly/Data_Preparation/raw_videos/ -name "*.mp4" -o -name "*.avi" -o -name "*.mov"
```
