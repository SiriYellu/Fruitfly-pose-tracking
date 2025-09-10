@echo off
echo Preparing video data for transfer...
set "SOURCE_DIR=C:\Users\siriy\Kennesaw State University\Dal Hyung Kim - 2023 FlyVialImage_Data"
set "TEMP_DIR=C:\temp\fly_video_data"
if not exist "%TEMP_DIR%" mkdir "%TEMP_DIR%"
echo Copying video files...
for %%f in ("%SOURCE_DIR%\*.mp4") do copy "%%f" "%TEMP_DIR%\"
for %%f in ("%SOURCE_DIR%\*.avi") do copy "%%f" "%TEMP_DIR%\"
for %%f in ("%SOURCE_DIR%\*.mov") do copy "%%f" "%TEMP_DIR%\"
echo Video files prepared in: %TEMP_DIR%
echo Next: Compress and upload to server
pause
