# Task 4: Behavioral Feature Extraction - Summary Report

**Generated:** 2025-09-16 12:11:37

## Overview
This report summarizes the behavioral analysis results from tracked fruit fly data.

## Key Metrics

- **Total Tracks Analyzed:** 8847
- **Average Distance Traveled:** 0.32 ± 0.16 mm
- **Average Speed:** 0.08 ± 0.01 mm/s
- **Max Speed:** 0.37 ± 0.07 mm/s
- **Activity Level:** 0.58 ± 0.09
- **Movement Frequency:** 23.61 ± 10.73
- **Stationary Duration:** 0.69 ± 0.78 seconds
- **Turning Frequency:** 0.87 ± 0.05
- **Pose Variability:** 0.13 ± 0.04

## Region Occupancy

- **Time in Center:** 0.49 ± 0.24
- **Time in Edge:** 0.49 ± 0.23
- **Time in Corner:** 0.02 ± 0.07

## Trajectory Statistics

- **Average Trajectory Length:** 127.38 ± 61.73 frames
- **Average Duration:** 4.25 ± 2.06 seconds

## Behavioral Insights

### Movement Patterns
- Flies show an average activity level of 0.58, indicating high activity with frequent movement.
- The average movement frequency of 23.61 suggests frequent movement bouts throughout the observation period.

### Spatial Behavior
- Flies show a strong preference for the center region of the vial.

### Pose and Turning Behavior
- Turning frequency of 0.87 indicates frequent directional changes and complex movement patterns.
- Pose variability of 0.13 suggests dynamic body posture changes during movement.

## Files Generated

- `behavioral_metrics_detailed.csv` - Detailed metrics for each track
- `behavioral_summary.csv` - Summary statistics
- `behavioral_summary.json` - Summary statistics in JSON format
- `../visualizations/` - Comprehensive behavioral visualizations
  - `speed_analysis.png` - Speed distribution and relationships
  - `movement_analysis.png` - Movement pattern analysis
  - `region_analysis.png` - Spatial behavior analysis
  - `pose_analysis.png` - Pose and turning behavior
  - `correlation_matrix.png` - Metric correlations
  - `behavioral_dashboard.png` - Comprehensive summary dashboard

## Technical Details

- **Frame Rate:** 30 FPS
- **Pixel to mm Conversion:** 0.1 mm/pixel
- **Activity Threshold:** 0.5 mm/s
- **Stationary Threshold:** 0.1 mm/s
- **Turn Threshold:** 30 degrees

## Next Steps

1. Review the generated visualizations for behavioral insights
2. Compare behavioral metrics across different experimental conditions
3. Perform statistical analysis on the detailed metrics
4. Export data for further analysis in specialized software
