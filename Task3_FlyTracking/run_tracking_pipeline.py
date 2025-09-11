#!/usr/bin/env python3
"""
Complete Fly Tracking and Behavioral Analysis Pipeline
Runs Task 3 (Fly Tracking) and Task 4 (Behavioral Feature Extraction)
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path
import json
from datetime import datetime

def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {cmd}")
    print('='*60)
    
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print("✓ Success!")
        if result.stdout:
            print("Output:", result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error: {e}")
        if e.stdout:
            print("Stdout:", e.stdout)
        if e.stderr:
            print("Stderr:", e.stderr)
        return False

def check_dependencies():
    """Check if required dependencies are installed"""
    print("Checking dependencies...")
    
    required_packages = [
        'numpy', 'pandas', 'opencv-python', 'matplotlib', 'seaborn'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"Missing packages: {missing_packages}")
        print("Installing missing packages...")
        install_cmd = f"pip install {' '.join(missing_packages)}"
        if not run_command(install_cmd, "Installing dependencies"):
            return False
    
    print("✓ All dependencies available")
    return True

def run_tracking_analysis(data_dir, output_dir):
    """Run the pose estimation and fly tracking analysis"""
    print("\n" + "="*80)
    print("TASK 3: POSE ESTIMATION + FLY TRACKING")
    print("="*80)
    
    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Check if we have images or labels
    data_path = Path(data_dir)
    has_images = any(data_path.glob("*.jpg")) or any(data_path.glob("*.png"))
    has_labels = any(data_path.glob("*.txt"))
    
    if has_images:
        # Run integrated pose estimation + tracking
        print("📸 Images detected - Running pose estimation + tracking")
        tracking_cmd = f"python scripts/run_pose_estimation_and_tracking.py --image_dir {data_dir} --output_dir {output_dir}"
    elif has_labels:
        # Run tracking only (legacy mode)
        print("📄 Labels detected - Running tracking only")
        tracking_cmd = f"python fly_tracker.py --data_dir {data_dir} --output_dir {output_dir}/tracking_results"
    else:
        print("✗ No images or labels found in data directory!")
        return False
    
    if not run_command(tracking_cmd, "Running pose estimation and fly tracking analysis"):
        return False
    
    # Check if tracking results exist
    tracking_results = Path(output_dir) / "tracking_results"
    if not (tracking_results / "trajectories.json").exists():
        print("✗ Tracking results not found!")
        return False
    
    print("✓ Pose estimation and fly tracking completed successfully!")
    return True

def run_behavioral_analysis(tracking_output_dir, behavioral_output_dir):
    """Run the behavioral analysis"""
    print("\n" + "="*80)
    print("TASK 4: BEHAVIORAL FEATURE EXTRACTION")
    print("="*80)
    
    # Create output directory
    Path(behavioral_output_dir).mkdir(parents=True, exist_ok=True)
    
    # Run behavioral analysis
    trajectories_file = Path(tracking_output_dir) / "tracking_results" / "trajectories.json"
    behavioral_cmd = f"python behavioral_analyzer.py --trajectories_file {trajectories_file} --output_dir {behavioral_output_dir}/behavioral_analysis"
    
    if not run_command(behavioral_cmd, "Running behavioral analysis"):
        return False
    
    # Check if behavioral results exist
    behavioral_results = Path(behavioral_output_dir) / "behavioral_analysis"
    if not (behavioral_results / "behavioral_metrics.csv").exists():
        print("✗ Behavioral analysis results not found!")
        return False
    
    print("✓ Behavioral analysis completed successfully!")
    return True

def generate_final_report(tracking_dir, behavioral_dir, output_dir):
    """Generate a comprehensive final report"""
    print("\n" + "="*80)
    print("GENERATING FINAL REPORT")
    print("="*80)
    
    report = {
        "analysis_timestamp": datetime.now().isoformat(),
        "pipeline_version": "1.0",
        "tasks_completed": ["Task 3: Fly Tracking", "Task 4: Behavioral Feature Extraction"],
        "results_summary": {}
    }
    
    # Load tracking results
    tracking_results = Path(tracking_dir) / "tracking_results"
    if (tracking_results / "tracking_stats.json").exists():
        with open(tracking_results / "tracking_stats.json", 'r') as f:
            tracking_stats = json.load(f)
            report["results_summary"]["tracking"] = tracking_stats
    
    # Load behavioral results
    behavioral_results = Path(behavioral_dir) / "behavioral_analysis"
    if (behavioral_results / "behavioral_summary.json").exists():
        with open(behavioral_results / "behavioral_summary.json", 'r') as f:
            behavioral_stats = json.load(f)
            report["results_summary"]["behavioral"] = behavioral_stats
    
    # Save final report
    report_file = Path(output_dir) / "final_report.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    # Generate markdown report
    generate_markdown_report(report, output_dir)
    
    print(f"✓ Final report generated: {report_file}")
    return True

def generate_markdown_report(report, output_dir):
    """Generate a markdown summary report"""
    md_content = f"""# Fly Tracking and Behavioral Analysis Report

**Analysis Date:** {report['analysis_timestamp']}
**Pipeline Version:** {report['pipeline_version']}

## Tasks Completed
- ✅ Task 3: Fly Tracking
- ✅ Task 4: Behavioral Feature Extraction

## Results Summary

### Tracking Results
"""
    
    if "tracking" in report["results_summary"]:
        tracking = report["results_summary"]["tracking"]
        md_content += f"""
- **Total Tracks:** {tracking.get('total_tracks', 'N/A')}
- **Active Tracks:** {tracking.get('active_tracks', 'N/A')}
- **Average Track Length:** {tracking.get('avg_track_length', 'N/A'):.2f} frames
- **Max Track Length:** {tracking.get('max_track_length', 'N/A')} frames
- **Min Track Length:** {tracking.get('min_track_length', 'N/A')} frames
"""
    
    md_content += "\n### Behavioral Analysis Results\n"
    
    if "behavioral" in report["results_summary"]:
        behavioral = report["results_summary"]["behavioral"]
        md_content += f"""
- **Total Tracks Analyzed:** {behavioral.get('total_tracks', 'N/A')}
"""
        
        if "summary_statistics" in behavioral:
            stats = behavioral["summary_statistics"]
            md_content += f"""
#### Key Behavioral Metrics
- **Average Speed:** {stats.get('avg_speed', {}).get('mean', 'N/A'):.4f} ± {stats.get('avg_speed', {}).get('std', 'N/A'):.4f}
- **Total Distance:** {stats.get('total_distance', {}).get('mean', 'N/A'):.4f} ± {stats.get('total_distance', {}).get('std', 'N/A'):.4f}
- **Activity Level:** {stats.get('activity_level', {}).get('mean', 'N/A'):.4f} ± {stats.get('activity_level', {}).get('std', 'N/A'):.4f}
- **Movement Frequency:** {stats.get('movement_frequency', {}).get('mean', 'N/A'):.2f} ± {stats.get('movement_frequency', {}).get('std', 'N/A'):.2f}
- **Turning Frequency:** {stats.get('turning_frequency', {}).get('mean', 'N/A'):.4f} ± {stats.get('turning_frequency', {}).get('std', 'N/A'):.4f}
"""
    
    md_content += f"""
## Output Files

### Tracking Results
- `tracking_results/tracks_summary.csv` - Summary of all tracks
- `tracking_results/frames_summary.csv` - Frame-by-frame tracking data
- `tracking_results/trajectories.json` - Detailed trajectory data
- `tracking_results/tracking_stats.json` - Tracking statistics

### Behavioral Analysis
- `behavioral_analysis/behavioral_metrics.csv` - Individual fly behavioral metrics
- `behavioral_analysis/behavioral_summary.json` - Summary statistics
- `behavioral_analysis/behavioral_analysis.png` - Behavioral distribution plots
- `behavioral_analysis/region_occupancy.png` - Vial region occupancy plot

## Next Steps

1. **Review Tracking Quality:** Check the tracking results for any ID switches or missed detections
2. **Validate Behavioral Metrics:** Examine the behavioral metrics for biological relevance
3. **Statistical Analysis:** Perform statistical tests comparing different conditions or time periods
4. **Visualization:** Create additional plots for specific research questions

## Notes

- All coordinates are normalized (0-1 range)
- Speed calculations assume 30 FPS frame rate
- Activity bouts require minimum 5 consecutive frames of movement
- Pose variability is calculated using head keypoint positions
"""
    
    # Save markdown report
    md_file = Path(output_dir) / "analysis_report.md"
    with open(md_file, 'w') as f:
        f.write(md_content)
    
    print(f"✓ Markdown report generated: {md_file}")

def main():
    parser = argparse.ArgumentParser(description='Complete Fly Tracking and Behavioral Analysis Pipeline')
    parser.add_argument('--data_dir', type=str,
                       default='/mnt/storage5/Fruitfly/Extracted_Frames_task',
                       help='Directory containing images or labeled data')
    parser.add_argument('--output_dir', type=str,
                       default='/mnt/storage5/Fruitfly/analysis_results',
                       help='Output directory for all results')
    parser.add_argument('--skip_dependencies', action='store_true',
                       help='Skip dependency checking')
    
    args = parser.parse_args()
    
    print("="*80)
    print("FLY TRACKING AND BEHAVIORAL ANALYSIS PIPELINE")
    print("="*80)
    print(f"Data directory: {args.data_dir}")
    print(f"Output directory: {args.output_dir}")
    print("="*80)
    
    # Check if data directory exists
    if not Path(args.data_dir).exists():
        print(f"✗ Data directory not found: {args.data_dir}")
        return 1
    
    # Check dependencies
    if not args.skip_dependencies:
        if not check_dependencies():
            print("✗ Dependency check failed!")
            return 1
    
    # Create output directory
    Path(args.output_dir).mkdir(parents=True, exist_ok=True)
    
    # Run tracking analysis
    tracking_success = run_tracking_analysis(args.data_dir, args.output_dir)
    if not tracking_success:
        print("✗ Tracking analysis failed!")
        return 1
    
    # Run behavioral analysis
    behavioral_success = run_behavioral_analysis(args.output_dir, args.output_dir)
    if not behavioral_success:
        print("✗ Behavioral analysis failed!")
        return 1
    
    # Generate final report
    report_success = generate_final_report(args.output_dir, args.output_dir, args.output_dir)
    if not report_success:
        print("✗ Report generation failed!")
        return 1
    
    print("\n" + "="*80)
    print("🎉 PIPELINE COMPLETED SUCCESSFULLY! 🎉")
    print("="*80)
    print(f"All results saved to: {args.output_dir}")
    print("\nKey output files:")
    print(f"  - Tracking results: {args.output_dir}/tracking_results/")
    print(f"  - Behavioral analysis: {args.output_dir}/behavioral_analysis/")
    print(f"  - Final report: {args.output_dir}/analysis_report.md")
    print("="*80)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
