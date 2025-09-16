# Task 4: Behavioral Feature Extraction

## Overview
This task implements comprehensive behavioral analysis of tracked fruit fly data, extracting detailed metrics and generating professional visualizations to understand movement patterns, spatial behavior, and pose dynamics. Features a **professional color palette** optimized for research publications and scientific presentations.

##  Key Features

###  **Advanced Behavioral Metrics**
- **Speed Analysis**: Average speed, maximum speed, speed distribution with statistical analysis
- **Distance Metrics**: Total distance traveled, movement patterns, trajectory analysis
- **Activity Patterns**: Movement frequency, activity level, stationary duration analysis
- **Spatial Behavior**: Time spent in center, edge, and corner regions with preference analysis
- **Pose Dynamics**: Pose variability, turning frequency, body posture changes
- **Temporal Analysis**: Duration, trajectory length, behavioral trends over time

###  **Comprehensive Research Visualizations**
- **Professional color palette** optimized for research publications
- **Multiple chart types**: histograms, scatter plots, box plots, heatmaps, pie charts
- **Statistical analysis** with mean, standard deviation, and significance testing
- **Behavioral clustering** using K-means algorithm
- **Time series analysis** for temporal patterns
- **Spatial behavior analysis** with region preferences
- **Correlation analysis** with detailed heatmaps

###  **Research-Focused Chart Types**
- **Statistical Analysis**: Box plots, histograms, distribution analysis
- **Correlation Heatmaps**: Detailed metric relationships
- **Time Series Plots**: Temporal behavioral patterns
- **Behavioral Clustering**: K-means clustering analysis
- **Spatial Analysis**: Region occupancy and preferences
- **Comprehensive Dashboards**: Multi-panel research summaries

## 🗂️ Directory Structure

```
Task4_BehavioralAnalysis/
├── scripts/
│   ├── behavioral_analyzer.py          # Core behavioral analysis engine
│   └── behavioral_visualizer.py       # Standard visualization generation
├── results/                            # Analysis results (generated)
│   ├── behavioral_metrics_detailed.csv
│   ├── behavioral_summary.csv
│   ├── behavioral_summary.json
│   └── TASK4_SUMMARY.md
├── visualizations/                     # Generated visualizations
│   ├── behavioral_dashboard.png            # Comprehensive dashboard
│   ├── speed_analysis.png                  # Speed distributions
│   ├── movement_analysis.png               # Movement patterns
│   ├── region_analysis.png                 # Spatial behavior
│   ├── pose_analysis.png                   # Pose dynamics
│   └── correlation_matrix.png              # Metric correlations
├── data/                              # Input data (if needed)
├── run_behavioral_analysis.py         # Main pipeline script
└── README.md                          # This file
```

##  Usage

### Quick Start
```bash
# Run complete behavioral analysis pipeline
python run_behavioral_analysis.py

# With custom parameters
python run_behavioral_analysis.py \
    --trajectories_file /path/to/trajectories.json \
    --output_dir /path/to/output \
    --frame_rate 30.0 \
    --pixel_to_mm 0.1

# Generate standard behavioral visualizations
python scripts/behavioral_visualizer.py --metrics_file results/behavioral_metrics_detailed.csv --summary_file results/behavioral_summary.json --output_dir visualizations
```

### Command Line Options

| Option | Default | Description |
|--------|---------|-------------|
| `--trajectories_file` | Task3 results | Path to trajectories JSON from Task 3 |
| `--output_dir` | `results/` | Output directory for analysis results |
| `--frame_rate` | `30.0` | Video frame rate (FPS) |
| `--pixel_to_mm` | `0.1` | Pixel to millimeter conversion factor |
| `--skip_prereq_check` | `False` | Skip prerequisite validation |
| `--skip_visualization` | `False` | Skip visualization generation |

##  Behavioral Metrics

###  **Movement Metrics**
- **Total Distance**: Cumulative distance traveled (mm)
- **Average Speed**: Mean speed over trajectory (mm/s)
- **Max Speed**: Peak speed achieved (mm/s)
- **Movement Frequency**: Number of active movement periods
- **Activity Level**: Proportion of time spent moving (0-1)
- **Stationary Duration**: Total time spent stationary (seconds)

###  **Spatial Metrics**
- **Time in Center**: Proportion of time in center region
- **Time in Edge**: Proportion of time in edge region
- **Time in Corner**: Proportion of time in corner region
- **Region Preference**: Primary region classification

###  **Pose Metrics**
- **Pose Variability**: Variance in body posture across frames
- **Turning Frequency**: Rate of directional changes
- **Body Stability**: Consistency of pose orientation

###  **Temporal Metrics**
- **Trajectory Length**: Number of frames in track
- **Duration**: Total time of track (seconds)
- **Start/End Time**: Frame identifiers for track boundaries



##  Output Files

### 📈 **Data Files**
- `behavioral_metrics_detailed.csv` - Complete metrics for each track
- `behavioral_summary.csv` - Statistical summary
- `behavioral_summary.json` - Summary in JSON format
- `TASK4_SUMMARY.md` - Comprehensive analysis report

##  Technical Implementation

### Core Classes
- **`BehavioralAnalyzer`**: Main analysis engine with advanced metrics calculation
- **`BehavioralVisualizer`**: Professional visualization generation with research-grade styling
- **`BehavioralMetrics`**: Data container for individual track metrics

### Key Algorithms
- **Speed Calculation**: Instantaneous speed with pixel-to-mm conversion
- **Region Classification**: Spatial region assignment (center/edge/corner)
- **Pose Variability**: Head position variance calculation
- **Activity Detection**: Movement bout detection with configurable thresholds
- **K-means Clustering**: Behavioral pattern classification using scikit-learn
- **Statistical Analysis**: Comprehensive statistical testing and analysis
- **Correlation Analysis**: Pearson and Spearman correlation calculations



##  Results Summary 

### Key Statistics 
- **Total Tracks**: 8,847  (Updated from Task 3)
- **Total Distance**: 3.19 ± 1.55 (normalized units) 
- **Average Speed**: 0.78 ± 0.14 (normalized units/second) 
- **Max Speed**: 3.70 ± 0.71 (normalized units/second) 
- **Activity Level**: 73.18% ± 10.42% (high activity) 
- **Movement Frequency**: 18.70 ± 9.09 (activity bouts per track) 
- **Stationary Duration**: 1.24 ± 0.95 (seconds) 
- **Turning Frequency**: 76.22 ± 4.75 (direction changes per 100 frames) 

### Region Occupancy 
- **Time in Center**: 53.19% ± 23.31% 
- **Time in Edge**: 43.76% ± 20.36% 
- **Time in Corner**: 3.00% ± 10.80% 

### Behavioral Insights 
- **High activity levels** (73.18% active time) with clear movement patterns 
- **Moderate movement frequency** (18.7 bouts per track) indicates active exploration behavior 
- **Center preference** (53.19% time) shows flies prefer the center area 
- **Balanced edge usage** (43.76% time) indicates flies also use edge areas 
- **Minimal corner usage** (3.00% time) shows flies avoid extreme corners 
- **Stationary periods** (1.24 ± 0.95 seconds) show natural rest behavior 
- **High turning frequency** (76.22 ± 4.75 per 100 frames) indicates active navigation 



**Key Achievement**: Successfully created a complete behavioral analysis pipeline with professional visualizations optimized for scientific research and publication. The system now processes **8,847 tracks** (updated from Task 3) with realistic behavioral metrics including high activity levels (73.18%), moderate movement frequency (18.7 bouts per track), and comprehensive spatial behavior analysis showing balanced distribution across center (27.39%), edge (54.33%), and corner (18.28%) regions.
