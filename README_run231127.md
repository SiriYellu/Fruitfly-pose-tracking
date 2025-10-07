# Task 4: 24-Hour Behavioral Analysis -Implementation Report

## Overview
This document summarizes the complete implementation of Task 4: 24-Hour Behavioral Analysis for fruit fly tracking data. The analysis processes 24 hours of video data from run 231127 (November 27, 2023) using YOLOv11-Pose tracking and computes comprehensive behavioral metrics for scientific analysis.

## Experimental Setup
- **Date**: November 27, 2023 (Run 231127)
- **Duration**: 24 hours (48 clips × 30 minutes each)
- **Vial Configuration**: 5 total vial positions, 2 active vials
- **Active Vials**:
  - **Vial 28137**: LMB231120-11, 28 females, 1 male
  - **Vial 28142**: LMB231120-12, 11 females, 3 males
- **Frame Resolution**: ~2000px width, 30 FPS
- **Pixel-to-mm Conversion**: 0.0625 mm/px
- **Activity Threshold**: 2 px/frame (≈ 3.75 mm/s)

## Technical Implementation

### 1. YOLO Model and Tracking
- **Model**: YOLOv11-Pose (improved_fruitfly_pose_20250928_2323562)
- **Tracking Algorithm**: BYTETrack with Kalman filtering
- **Multi-GPU Processing**: 4 GPUs for parallel video processing
- **Output Format**: CSV per-frame and per-track data

## Methods: End-to-end pipeline and metric calculations (Run 231127)

This section explains, in detail, how videos are processed, how flies are detected and tracked, how speeds and activity are computed at the frame level, how detections are mapped to vials, how per-window metrics are aggregated, how bouts and stances are segmented, and how daily totals are produced for Run 231127.

### 1. Input videos and windows
- The dataset consists of 48 MP4 clips, each about 30 minutes; together they cover roughly 24 hours.
- Each clip is processed independently and contributes one 30 minute window per active vial.

### 2. Detection and tracking
- Detector: YOLOv11-Pose. For each frame, it returns bounding boxes and pose keypoints.
- Tracker: BYTETrack with Kalman filtering. It assigns and maintains a stable `track_id` for each fly across frames within a clip. Tracking is persisted per clip to bridge short occlusions.

### 3. Kinematic position and speed
- Position for kinematic calculations is the center of the bounding box, not the body keypoints.
- For a given `track_id`, between frames `t-1` and `t`:
  - `dx = x_t - x_{t-1}`, `dy = y_t - y_{t-1}` (pixels)
  - Per frame displacement `dist_px = sqrt(dx^2 + dy^2)`
  - Frame gap is usually 1; if it is larger, displacement is divided by the gap.
- Per frame speed: `speed_px_per_frame = dist_px / frame_gap`
- Unit conversion when needed: `speed_mm_s = speed_px_per_frame × FPS × PIXEL_TO_MM`
- Activity classification: a frame is active if `speed_px_per_frame ≥ 2` px/frame (≈ 3.75 mm/s at 30 FPS with 0.0625 mm/px).

### 4. Vial assignment
- The arena has five vial positions across the image width; only two are active in this run.
- We divide the image width into five equal bins and assign each detection to a vial by x coordinate of its bounding box center.
- For Run 231127, only vials 28137 and 28142 are kept; detections mapped to other positions are excluded from downstream metrics.

### 5. Per window aggregation (per active vial, per 30 minute clip)
For each active vial in a clip we compute:
- Average number of flies detected per frame: for each frame, count unique `track_id`, then average across frames.
- Average number of active flies per frame: same, but only frames where `is_active == 1` are counted for the numerator.
- Average speed (mm/s) for all flies: mean of `speed_px_per_frame × FPS × PIXEL_TO_MM` across all rows for the vial.
- Average speed (mm/s) for active flies only: same as above, restricted to `is_active == 1`.
- Total travel distance per vial (mm): sum of `speed_px_per_frame × PIXEL_TO_MM` across all rows in the vial and window.

### 6. Bout and stance segmentation
- For each track within the vial and window, the `is_active` time series is scanned in frame order.
- Bout: maximal contiguous sequence of active frames. Stance: maximal contiguous sequence of inactive frames.
- For each bout we compute:
  - Bout duration (s) = frames in bout ÷ FPS
  - Bout distance (mm) = sum of `speed_px_per_frame` over the bout × `PIXEL_TO_MM`
- We collect all bouts and all stances across tracks and compute, at the vial level:
  - Average bout duration (s): mean over bout durations; 0 if there are no bouts
  - Average travel distance per bout (mm): mean over bout distances; 0 if there are no bouts
  - Average stance duration (s): mean over stance durations; 0 if there are no stances

### 7. Daily totals (per active vial)
- Total distance over the day (mm): sum of window level `total_distance_vial_mm` for that vial.
- Mean speed over the day (mm/s): mean of `avg_speed_all_mm_s` across that vial’s windows.
- Mean active rate over the day: `mean(avg_active_flies_per_frame) ÷ mean(avg_flies_per_frame)` across windows, approximating the fraction of flies active in a typical frame.

### 8. Units and constants
- FPS: 30
- Pixel to mm: 0.0625 mm/px
- Activity threshold: 2 px/frame (≈ 3.75 mm/s)
- Window length: 30 minutes (54,000 frames when all frames are present)

### 9. Files produced and naming
- Per clip CSVs in `02_CSVs/`:
  - `FVI_..._frames.csv`: per frame rows including `track_id`, position, `speed_px_per_frame`, and `is_active`
  - `FVI_..._tracks.csv`: per track summaries including total distance and mean speed
- Per window metrics: `03_Metrics/20231127_window_metrics.csv`
  - One row per active vial per clip with the eight metrics listed above
- Daily totals: `03_Metrics/20231127_daily_totals.csv`
  - One row per active vial with day level aggregates

### 10. Quality checks
- Tracking continuity: verified via monotonic frame indices per `track_id` and nonzero durations.
- Vial mapping: deterministic by x coordinate and image width; filtered to the two active vials.
- Safe aggregation: empty sets yield 0 for the corresponding averages (for example no bouts in a window).
- Threshold validation: minimum active speed equals the threshold in mm/s within rounding tolerance.

### 1.1 Speed Measurement Methodology
**Important**: Fly speed is calculated using the **center of the bounding box**, not body keypoints:

- **Position**: Center of detection bounding box
  - `x_center = (bbox[0] + bbox[2]) / 2`
  - `y_center = (bbox[1] + bbox[3]) / 2`
  
- **Speed Calculation**: Euclidean distance between consecutive detections
  - `distance = sqrt((x_curr - x_prev)² + (y_curr - y_prev)²)`
  - `speed_px_per_frame = distance / frame_difference`
  - Converted to mm/s: `speed_mm_s = speed_px_per_frame × FPS × PIXEL_TO_MM`
  
- **Note**: Although YOLOv11-Pose detects body keypoints (head, thorax, abdomen), these are **not used** for speed calculations - only the bounding box center is tracked for movement

### 2. Data Processing Pipeline
```
Raw Videos → YOLO Detection → BYTETrack → CSV Export → Metrics Computation → Visualization
```

**Processing Steps**:
1. **Video Processing**: 48 video clips (30 minutes each)
2. **Fly Detection**: YOLOv11-Pose keypoint detection
3. **Track Association**: BYTETrack for ID persistence
4. **Data Export**:  CSV formats
5. **Vial Assignment**: X-coordinate mapping to vial IDs
6. **Metrics Computation**: 8 behavioral metrics per 30-minute window
7. **Visualization**: Time-series plots and comparisons

### 3. Behavioral Metrics Computed
For each vial, per 30-minute segment, we compute:

1. **Average number of flies detected per frame**
2. **Average number of active flies per frame** (speed > 2 px/frame)
3. **Average speed (mm/s) across all detected flies**
4. **Average speed (mm/s) for active flies only**
5. **Average bout duration (s)** - continuous active periods
6. **Average travel distance per bout (mm)**
7. **Average stance duration (s)** - continuous inactive periods
8. **Total travel distance per vial (mm)**

## Output Files Generated

### 1. Raw Tracking Data
- **Per-Frame CSV**: `*_frames.csv` - Individual fly positions per frame
- **Per-Track CSV**: `*_tracks.csv` - Track summaries and statistics

### 2. Computed Metrics
- **Window Metrics**: `20231127_window_metrics.csv` (96 rows)
  - 48 time windows × 2 vials
  - All 8 metrics per window per vial
- **Daily Totals**: `20231127_daily_totals.csv` (2 rows)
  - Aggregated metrics for entire 24-hour period per vial

### 3. Visualizations
**Original Analysis Plots**:
- `20231127_speed_timeseries.png` - Speed over time
- `20231127_active_rate_timeseries.png` - Activity rate over time
- `20231127_cumulative_distance.png` - Cumulative distance
- `20231127_speed_comparison.png` - Speed comparisons

**Professor-Requested Plots**:
- `professor_detected_flies_per_frame.png` - Average flies detected over time
- `professor_moving_flies_per_frame.png` - Average moving flies over time
- `professor_average_speed_per_vial.png` - Speed comparisons (all vs moving)
- `professor_travel_distance.png` - Travel distance analysis
- `professor_segmented_timeseries.png` - Hourly segmented analysis
- `professor_comparison_plots.png` - Multi-vial comparisons

**Speed Distribution Analysis**:
- `speed_histogram_moving_flies.png` - Histogram of speeds for moving flies (linear & log scale)
- `speed_histogram_comparison.png` - Comparison of all flies vs moving flies speeds

## Key Results

### Vial Performance Summary
**Vial 28137** (LMB231120-11, 28 females, 1 male):
- Total distance: 258.9 meters over 24 hours
- Mean speed: 1.52 mm/s
- Active rate: 51.8%
- 48 time windows analyzed

**Vial 28142** (LMB231120-12, 11 females, 3 males):
- Total distance: 768.7 meters over 24 hours
- Mean speed: 0.95 mm/s
- Active rate: 15.0%
- 48 time windows analyzed

### Behavioral Insights
- **Vial 28142** shows significantly higher total movement (768.7m vs 258.9m)
- **Vial 28137** has higher average speed but lower total distance
- **Activity patterns** vary throughout the 24-hour period
- **Bout and stance durations** provide insights into movement patterns

### Speed Distribution Analysis
From 24-hour analysis (45,879,874 total detections):
- **Active flies**: 3,306,761 detections (7.21% of total)
- **Mean speed (moving flies)**: 8.55 mm/s
- **Median speed (moving flies)**: 7.46 mm/s
- **Standard deviation**: 4.88 mm/s
- **Speed range**: 3.75 - 414.55 mm/s
- **99th percentile**: 21.58 mm/s

**Distribution Characteristics**:
- Speed distribution is right-skewed with most speeds between 4-12 mm/s
- Log-scale histogram reveals long tail of high-speed movements
- Activity threshold (3.75 mm/s) effectively separates moving from stationary flies
- Rare high-speed events (>20 mm/s) represent fast locomotion or tracking jumps

## Technical Specifications

### System Requirements
- **GPU**: 4× NVIDIA GPUs for parallel processing
- **Storage**: ~500GB for raw videos and processed data

### Data Quality
- **Track Continuity**: Maintained through BYTETrack algorithm
- **Detection Accuracy**: YOLOv11-Pose model trained on fruit fly data
- **Temporal Resolution**: 30 FPS frame rate
- **Spatial Resolution**: Sub-millimeter precision (0.0625 mm/px)

### Validation and Quality Control
- **Vial Assignment**: Verified against physical setup
- **Metric Calculations**: Cross-validated with manual spot checks


## File Structure
```
Task4_BehavioralAnalysis/
├── 02_CSVs/                    # Raw tracking data
│   ├── *_frames.csv           # Per-frame data
│   └── *_tracks.csv           # Per-track summaries
├── 03_Metrics/                 # Computed metrics
│   ├── 20231127_window_metrics.csv
│   └── 20231127_daily_totals.csv
└── 05_Scripts/                 # Analysis scripts
    ├── process_24hour_day.py
    ├── compute_metrics_adapted.py
    └── create_plots.py
```

## Methodology Validation

### Vial Assignment Logic
- **X-coordinate mapping**: `vial_id = int(x_px // 400) + 1`
- **Active vial filtering**: Only vials 28137 and 28142 included in analysis

### Metric Computation
- **Temporal aggregation**: 30-minute windows (54,000 frames each)
- **Spatial aggregation**: Per-vial analysis
- **Activity threshold**: 2 px/frame (3.75 mm/s) for active fly classification
- **Bout detection**: Continuous periods above threshold
- **Stance detection**: Continuous periods below threshold


## Conclusions

The 24-hour behavioral analysis pipeline successfully:

1. **Processed** 24 hours of fruit fly tracking data
2. **Computed** all 8 required behavioral metrics


The analysis reveals distinct behavioral patterns between the two vials, with significant differences in total movement, speed profiles, and activity rates. The data provides a solid foundation for further behavioral studies and comparative analysis.


---

### Recent Additions (October 6, 2025)
- **Speed Histogram Analysis**: Added detailed speed distribution plots for moving flies
- **Methodology Documentation**: Documented that speed is measured using bounding box center (not body keypoints)
- **Distribution Statistics**: Computed comprehensive statistics from 45M+ detections across 24 hours
