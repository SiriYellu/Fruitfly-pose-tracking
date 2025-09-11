#!/usr/bin/env python3
"""
Task 4: Behavioral Feature Extraction Pipeline
Main script to run comprehensive behavioral analysis
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path
from datetime import datetime

def run_command(command: str, description: str) -> bool:
    """Run a command and return success status"""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {command}")
    print('='*60)
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print("✓ Command completed successfully")
        if result.stdout:
            print("Output:", result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Command failed with error: {e}")
        if e.stdout:
            print("Stdout:", e.stdout)
        if e.stderr:
            print("Stderr:", e.stderr)
        return False

def check_prerequisites():
    """Check if required files and dependencies exist"""
    print("Checking prerequisites...")
    
    # Check if Task 3 results exist
    trajectories_file = "/mnt/storage5/Fruitfly/Task3_FlyTracking/results/tracking_results/trajectories.json"
    if not os.path.exists(trajectories_file):
        print(f"✗ Trajectories file not found: {trajectories_file}")
        print("Please run Task 3 first to generate tracking results")
        return False
    
    print(f"✓ Found trajectories file: {trajectories_file}")
    
    # Check Python dependencies
    required_packages = ['numpy', 'pandas', 'matplotlib', 'seaborn', 'scipy']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package} is available")
        except ImportError:
            missing_packages.append(package)
            print(f"✗ {package} is missing")
    
    if missing_packages:
        print(f"Please install missing packages: {', '.join(missing_packages)}")
        return False
    
    return True

def run_behavioral_analysis(trajectories_file: str, output_dir: str, frame_rate: float = 30.0, pixel_to_mm: float = 0.1):
    """Run behavioral feature extraction"""
    print("\n" + "="*80)
    print("TASK 4: BEHAVIORAL FEATURE EXTRACTION")
    print("="*80)
    
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Run behavioral analysis
    analysis_cmd = f"python scripts/behavioral_analyzer.py --trajectories_file {trajectories_file} --output_dir {output_dir} --frame_rate {frame_rate} --pixel_to_mm {pixel_to_mm}"
    
    if not run_command(analysis_cmd, "Running behavioral feature extraction"):
        return False
    
    # Check if analysis completed successfully
    metrics_file = Path(output_dir) / "behavioral_metrics_detailed.csv"
    summary_file = Path(output_dir) / "behavioral_summary.json"
    
    if not metrics_file.exists() or not summary_file.exists():
        print("✗ Behavioral analysis results not found!")
        return False
    
    print("✓ Behavioral feature extraction completed successfully!")
    return True

def run_visualization(output_dir: str):
    """Run behavioral analysis visualization"""
    print("\n" + "="*60)
    print("CREATING BEHAVIORAL VISUALIZATIONS")
    print("="*60)
    
    metrics_file = Path(output_dir) / "behavioral_metrics_detailed.csv"
    summary_file = Path(output_dir) / "behavioral_summary.json"
    viz_dir = Path(output_dir).parent / "visualizations"
    
    if not metrics_file.exists() or not summary_file.exists():
        print("✗ Required analysis files not found!")
        return False
    
    # Run visualization
    viz_cmd = f"python scripts/behavioral_visualizer.py --metrics_file {metrics_file} --summary_file {summary_file} --output_dir {viz_dir}"
    
    if not run_command(viz_cmd, "Creating behavioral visualizations"):
        return False
    
    print("✓ Behavioral visualizations completed successfully!")
    return True

def generate_summary_report(output_dir: str):
    """Generate a comprehensive summary report"""
    print("\n" + "="*60)
    print("GENERATING SUMMARY REPORT")
    print("="*60)
    
    summary_file = Path(output_dir) / "behavioral_summary.json"
    if not summary_file.exists():
        print("✗ Summary file not found!")
        return False
    
    import json
    with open(summary_file, 'r') as f:
        summary = json.load(f)
    
    report_file = Path(output_dir) / "TASK4_SUMMARY.md"
    
    with open(report_file, 'w') as f:
        f.write("# Task 4: Behavioral Feature Extraction - Summary Report\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("## Overview\n")
        f.write("This report summarizes the behavioral analysis results from tracked fruit fly data.\n\n")
        
        f.write("## Key Metrics\n\n")
        f.write(f"- **Total Tracks Analyzed:** {summary['total_tracks']}\n")
        f.write(f"- **Average Distance Traveled:** {summary['total_distance_mean']:.2f} ± {summary['total_distance_std']:.2f} mm\n")
        f.write(f"- **Average Speed:** {summary['average_speed_mean']:.2f} ± {summary['average_speed_std']:.2f} mm/s\n")
        f.write(f"- **Max Speed:** {summary['max_speed_mean']:.2f} ± {summary['max_speed_std']:.2f} mm/s\n")
        f.write(f"- **Activity Level:** {summary['activity_level_mean']:.2f} ± {summary['activity_level_std']:.2f}\n")
        f.write(f"- **Movement Frequency:** {summary['movement_frequency_mean']:.2f} ± {summary['movement_frequency_std']:.2f}\n")
        f.write(f"- **Stationary Duration:** {summary['stationary_duration_mean']:.2f} ± {summary['stationary_duration_std']:.2f} seconds\n")
        f.write(f"- **Turning Frequency:** {summary['turning_frequency_mean']:.2f} ± {summary['turning_frequency_std']:.2f}\n")
        f.write(f"- **Pose Variability:** {summary['pose_variability_mean']:.2f} ± {summary['pose_variability_std']:.2f}\n\n")
        
        f.write("## Region Occupancy\n\n")
        f.write(f"- **Time in Center:** {summary['time_in_center_mean']:.2f} ± {summary['time_in_center_std']:.2f}\n")
        f.write(f"- **Time in Edge:** {summary['time_in_edge_mean']:.2f} ± {summary['time_in_edge_std']:.2f}\n")
        f.write(f"- **Time in Corner:** {summary['time_in_corner_mean']:.2f} ± {summary['time_in_corner_std']:.2f}\n\n")
        
        f.write("## Trajectory Statistics\n\n")
        f.write(f"- **Average Trajectory Length:** {summary['trajectory_length_mean']:.2f} ± {summary['trajectory_length_std']:.2f} frames\n")
        f.write(f"- **Average Duration:** {summary['duration_mean']:.2f} ± {summary['duration_std']:.2f} seconds\n\n")
        
        f.write("## Behavioral Insights\n\n")
        f.write("### Movement Patterns\n")
        f.write(f"- Flies show an average activity level of {summary['activity_level_mean']:.2f}, indicating ")
        if summary['activity_level_mean'] > 0.5:
            f.write("high activity with frequent movement.\n")
        else:
            f.write("moderate activity with periods of rest.\n")
        
        f.write(f"- The average movement frequency of {summary['movement_frequency_mean']:.2f} suggests ")
        if summary['movement_frequency_mean'] > 10:
            f.write("frequent movement bouts throughout the observation period.\n")
        else:
            f.write("sporadic movement patterns.\n")
        
        f.write("\n### Spatial Behavior\n")
        center_preference = summary['time_in_center_mean']
        if center_preference > 0.4:
            f.write("- Flies show a strong preference for the center region of the vial.\n")
        elif center_preference > 0.2:
            f.write("- Flies show moderate preference for the center region.\n")
        else:
            f.write("- Flies show preference for edge/corner regions over the center.\n")
        
        f.write("\n### Pose and Turning Behavior\n")
        f.write(f"- Turning frequency of {summary['turning_frequency_mean']:.2f} indicates ")
        if summary['turning_frequency_mean'] > 0.3:
            f.write("frequent directional changes and complex movement patterns.\n")
        else:
            f.write("relatively straight movement patterns.\n")
        
        f.write(f"- Pose variability of {summary['pose_variability_mean']:.2f} suggests ")
        if summary['pose_variability_mean'] > 0.1:
            f.write("dynamic body posture changes during movement.\n")
        else:
            f.write("relatively stable body posture during movement.\n")
        
        f.write("\n## Files Generated\n\n")
        f.write("- `behavioral_metrics_detailed.csv` - Detailed metrics for each track\n")
        f.write("- `behavioral_summary.csv` - Summary statistics\n")
        f.write("- `behavioral_summary.json` - Summary statistics in JSON format\n")
        f.write("- `../visualizations/` - Comprehensive behavioral visualizations\n")
        f.write("  - `speed_analysis.png` - Speed distribution and relationships\n")
        f.write("  - `movement_analysis.png` - Movement pattern analysis\n")
        f.write("  - `region_analysis.png` - Spatial behavior analysis\n")
        f.write("  - `pose_analysis.png` - Pose and turning behavior\n")
        f.write("  - `correlation_matrix.png` - Metric correlations\n")
        f.write("  - `behavioral_dashboard.png` - Comprehensive summary dashboard\n\n")
        
        f.write("## Technical Details\n\n")
        f.write("- **Frame Rate:** 30 FPS\n")
        f.write("- **Pixel to mm Conversion:** 0.1 mm/pixel\n")
        f.write("- **Activity Threshold:** 0.5 mm/s\n")
        f.write("- **Stationary Threshold:** 0.1 mm/s\n")
        f.write("- **Turn Threshold:** 30 degrees\n\n")
        
        f.write("## Next Steps\n\n")
        f.write("1. Review the generated visualizations for behavioral insights\n")
        f.write("2. Compare behavioral metrics across different experimental conditions\n")
        f.write("3. Perform statistical analysis on the detailed metrics\n")
        f.write("4. Export data for further analysis in specialized software\n")
    
    print(f"✓ Summary report generated: {report_file}")
    return True

def main():
    parser = argparse.ArgumentParser(description='Task 4: Behavioral Feature Extraction Pipeline')
    parser.add_argument('--trajectories_file', type=str,
                       default='/mnt/storage5/Fruitfly/Task3_FlyTracking/results/tracking_results/trajectories.json',
                       help='Path to trajectories JSON file from Task 3')
    parser.add_argument('--output_dir', type=str,
                       default='/mnt/storage5/Fruitfly/Task4_BehavioralAnalysis/results',
                       help='Output directory for behavioral analysis results')
    parser.add_argument('--frame_rate', type=float, default=30.0,
                       help='Frame rate of the video (FPS)')
    parser.add_argument('--pixel_to_mm', type=float, default=0.1,
                       help='Pixel to millimeter conversion factor')
    parser.add_argument('--skip_prereq_check', action='store_true',
                       help='Skip prerequisite checks')
    parser.add_argument('--skip_visualization', action='store_true',
                       help='Skip visualization generation')
    
    args = parser.parse_args()
    
    print("="*80)
    print("TASK 4: BEHAVIORAL FEATURE EXTRACTION")
    print("="*80)
    print(f"Trajectories file: {args.trajectories_file}")
    print(f"Output directory: {args.output_dir}")
    print(f"Frame rate: {args.frame_rate} FPS")
    print(f"Pixel to mm conversion: {args.pixel_to_mm}")
    
    # Check prerequisites
    if not args.skip_prereq_check:
        if not check_prerequisites():
            print("\n✗ Prerequisites not met. Please fix the issues above and try again.")
            return False
    
    # Run behavioral analysis
    if not run_behavioral_analysis(args.trajectories_file, args.output_dir, args.frame_rate, args.pixel_to_mm):
        print("\n✗ Behavioral analysis failed!")
        return False
    
    # Run visualization
    if not args.skip_visualization:
        if not run_visualization(args.output_dir):
            print("\n✗ Visualization generation failed!")
            return False
    
    # Generate summary report
    if not generate_summary_report(args.output_dir):
        print("\n✗ Summary report generation failed!")
        return False
    
    print("\n" + "="*80)
    print("TASK 4 COMPLETED SUCCESSFULLY!")
    print("="*80)
    print(f"Results saved to: {args.output_dir}")
    print(f"Visualizations saved to: {Path(args.output_dir).parent / 'visualizations'}")
    print("\nKey behavioral metrics extracted:")
    print("• Average speed and distance traveled")
    print("• Movement frequency and activity level")
    print("• Stationary duration and turning frequency")
    print("• Time spent in different vial regions")
    print("• Pose variability and behavioral patterns")
    print("\nComprehensive visualizations and summary report generated!")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)


