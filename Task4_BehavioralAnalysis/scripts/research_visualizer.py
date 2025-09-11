#!/usr/bin/env python3
"""
Research-Focused Behavioral Analysis Visualization
Creates comprehensive scientific visualizations for behavioral research
"""

import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import List, Dict, Tuple
import argparse
from matplotlib.patches import Rectangle
import matplotlib.patches as mpatches
from scipy import stats
from scipy.stats import pearsonr, spearmanr
import warnings
warnings.filterwarnings('ignore')

class ResearchBehavioralVisualizer:
    """Creates research-focused visualizations for behavioral analysis"""
    
    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Research-focused color palette
        self.colors = {
            'primary': '#2E86AB',      # Professional blue
            'secondary': '#A23B72',    # Deep purple
            'accent': '#F18F01',       # Orange
            'success': '#C73E1D',      # Red
            'info': '#3A7D44',         # Green
            'warning': '#F77F00',      # Amber
            'light': '#F8F9FA',        # Light gray
            'dark': '#212529',         # Dark gray
            'text': '#343A40',         # Dark text
            'grid': '#E9ECEF'          # Light grid
        }
        
        # Set scientific style
        plt.style.use('default')
        sns.set_palette("Set2")
        
        # Scientific font settings
        plt.rcParams.update({
            'font.size': 12,
            'font.family': 'sans-serif',
            'axes.labelcolor': self.colors['text'],
            'text.color': self.colors['text'],
            'axes.edgecolor': self.colors['dark'],
            'axes.linewidth': 1,
            'grid.color': self.colors['grid'],
            'grid.alpha': 0.7,
            'figure.facecolor': 'white',
            'axes.facecolor': 'white',
            'savefig.facecolor': 'white',
            'savefig.edgecolor': 'black',
            'savefig.dpi': 300
        })
        
    def load_data(self, metrics_file: str, summary_file: str) -> Tuple[pd.DataFrame, Dict]:
        """Load behavioral metrics and summary data"""
        metrics_df = pd.read_csv(metrics_file)
        
        with open(summary_file, 'r') as f:
            summary = json.load(f)
        
        return metrics_df, summary
    
    def create_comprehensive_dashboard(self, df: pd.DataFrame, summary: Dict):
        """Create a comprehensive research dashboard"""
        fig = plt.figure(figsize=(20, 16))
        fig.patch.set_facecolor('white')
        gs = fig.add_gridspec(4, 4, hspace=0.3, wspace=0.3)
        
        # Main title
        fig.suptitle('Fruit Fly Behavioral Analysis - Research Dashboard', 
                    fontsize=20, fontweight='bold', color=self.colors['dark'], y=0.95)
        
        # Key statistics panel
        ax1 = fig.add_subplot(gs[0, :2])
        ax1.axis('off')
        
        stats_text = f"""
        EXPERIMENTAL SUMMARY
        ═══════════════════════════════════════════════════════════════
        
        Sample Size: {summary['total_tracks']:,} tracks analyzed
        Average Distance: {summary['total_distance_mean']:.3f} ± {summary['total_distance_std']:.3f} mm
        Average Speed: {summary['average_speed_mean']:.3f} ± {summary['average_speed_std']:.3f} mm/s
        Max Speed: {summary['max_speed_mean']:.3f} ± {summary['max_speed_std']:.3f} mm/s
        Activity Level: {summary['activity_level_mean']:.3f} ± {summary['activity_level_std']:.3f}
        Movement Frequency: {summary['movement_frequency_mean']:.1f} ± {summary['movement_frequency_std']:.1f}
        Stationary Duration: {summary['stationary_duration_mean']:.2f} ± {summary['stationary_duration_std']:.2f} s
        Pose Variability: {summary['pose_variability_mean']:.3f} ± {summary['pose_variability_std']:.3f}
        """
        
        ax1.text(0.05, 0.5, stats_text, fontsize=11, verticalalignment='center',
                color=self.colors['text'], fontweight='normal',
                bbox=dict(boxstyle="round,pad=0.5", facecolor='white', 
                         edgecolor=self.colors['primary'], alpha=0.8, linewidth=1))
        
        # Speed distribution
        ax2 = fig.add_subplot(gs[0, 2:])
        n, bins, patches = ax2.hist(df['average_speed_mm_s'], bins=25, alpha=0.7, 
                                   color=self.colors['primary'], edgecolor='white', linewidth=1)
        ax2.set_xlabel('Average Speed (mm/s)', fontsize=12)
        ax2.set_ylabel('Frequency', fontsize=12)
        ax2.set_title('Speed Distribution', fontsize=14, fontweight='bold')
        ax2.axvline(df['average_speed_mm_s'].mean(), color=self.colors['accent'], 
                   linestyle='--', linewidth=2, label=f'Mean: {df["average_speed_mm_s"].mean():.3f}')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Activity level
        ax3 = fig.add_subplot(gs[1, :2])
        n, bins, patches = ax3.hist(df['activity_level'], bins=25, alpha=0.7, 
                                   color=self.colors['secondary'], edgecolor='white', linewidth=1)
        ax3.set_xlabel('Activity Level (0-1)', fontsize=12)
        ax3.set_ylabel('Frequency', fontsize=12)
        ax3.set_title('Activity Level Distribution', fontsize=14, fontweight='bold')
        ax3.axvline(df['activity_level'].mean(), color=self.colors['accent'], 
                   linestyle='--', linewidth=2, label=f'Mean: {df["activity_level"].mean():.3f}')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # Region occupancy
        ax4 = fig.add_subplot(gs[1, 2:])
        region_data = df[['time_in_center', 'time_in_edge', 'time_in_corner']].mean()
        region_colors = [self.colors['info'], self.colors['accent'], self.colors['success']]
        region_labels = ['Center', 'Edge', 'Corner']
        
        bars = ax4.bar(region_labels, region_data.values, color=region_colors, alpha=0.7, 
                      edgecolor='white', linewidth=1)
        ax4.set_ylabel('Average Time Proportion', fontsize=12)
        ax4.set_title('Spatial Behavior - Region Occupancy', fontsize=14, fontweight='bold')
        ax4.set_ylim(0, 1)
        ax4.grid(True, alpha=0.3, axis='y')
        
        # Add value labels
        for bar, v in zip(bars, region_data.values):
            ax4.text(bar.get_x() + bar.get_width()/2, v + 0.01, f'{v:.3f}', 
                    ha='center', va='bottom', fontsize=10)
        
        # Speed vs Distance
        ax5 = fig.add_subplot(gs[2, :2])
        scatter = ax5.scatter(df['total_distance_mm'], df['average_speed_mm_s'], 
                            alpha=0.6, c=df['activity_level'], cmap='viridis', 
                            s=50, edgecolors='white', linewidth=0.5)
        ax5.set_xlabel('Total Distance (mm)', fontsize=12)
        ax5.set_ylabel('Average Speed (mm/s)', fontsize=12)
        ax5.set_title('Speed vs Distance Relationship', fontsize=14, fontweight='bold')
        ax5.grid(True, alpha=0.3)
        
        # Add colorbar
        cbar = plt.colorbar(scatter, ax=ax5)
        cbar.set_label('Activity Level', fontsize=10)
        
        # Pose variability
        ax6 = fig.add_subplot(gs[2, 2:])
        n, bins, patches = ax6.hist(df['pose_variability'], bins=25, alpha=0.7, 
                                   color=self.colors['warning'], edgecolor='white', linewidth=1)
        ax6.set_xlabel('Pose Variability', fontsize=12)
        ax6.set_ylabel('Frequency', fontsize=12)
        ax6.set_title('Pose Variability Distribution', fontsize=14, fontweight='bold')
        ax6.axvline(df['pose_variability'].mean(), color=self.colors['accent'], 
                   linestyle='--', linewidth=2, label=f'Mean: {df["pose_variability"].mean():.3f}')
        ax6.legend()
        ax6.grid(True, alpha=0.3)
        
        # Movement frequency
        ax7 = fig.add_subplot(gs[3, :2])
        n, bins, patches = ax7.hist(df['movement_frequency'], bins=25, alpha=0.7, 
                                   color=self.colors['info'], edgecolor='white', linewidth=1)
        ax7.set_xlabel('Movement Frequency (bouts)', fontsize=12)
        ax7.set_ylabel('Frequency', fontsize=12)
        ax7.set_title('Movement Frequency Distribution', fontsize=14, fontweight='bold')
        ax7.axvline(df['movement_frequency'].mean(), color=self.colors['accent'], 
                   linestyle='--', linewidth=2, label=f'Mean: {df["movement_frequency"].mean():.1f}')
        ax7.legend()
        ax7.grid(True, alpha=0.3)
        
        # Activity vs Region time
        ax8 = fig.add_subplot(gs[3, 2:])
        ax8.scatter(df['time_in_center'], df['activity_level'], alpha=0.6, 
                   color=self.colors['info'], s=30, label='Center', edgecolors='white', linewidth=0.5)
        ax8.scatter(df['time_in_edge'], df['activity_level'], alpha=0.6, 
                   color=self.colors['accent'], s=30, label='Edge', edgecolors='white', linewidth=0.5)
        ax8.scatter(df['time_in_corner'], df['activity_level'], alpha=0.6, 
                   color=self.colors['success'], s=30, label='Corner', edgecolors='white', linewidth=0.5)
        
        ax8.set_xlabel('Time in Region', fontsize=12)
        ax8.set_ylabel('Activity Level', fontsize=12)
        ax8.set_title('Region Time vs Activity Level', fontsize=14, fontweight='bold')
        ax8.legend()
        ax8.grid(True, alpha=0.3)
        
        plt.savefig(self.output_dir / 'research_dashboard.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def create_statistical_analysis(self, df: pd.DataFrame):
        """Create comprehensive statistical analysis plots"""
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('Statistical Analysis of Behavioral Metrics', fontsize=16, fontweight='bold')
        
        # Box plots for key metrics
        metrics = ['average_speed_mm_s', 'total_distance_mm', 'activity_level', 
                  'movement_frequency', 'pose_variability', 'turning_frequency']
        titles = ['Average Speed (mm/s)', 'Total Distance (mm)', 'Activity Level', 
                 'Movement Frequency', 'Pose Variability', 'Turning Frequency']
        
        for i, (metric, title) in enumerate(zip(metrics, titles)):
            ax = axes[i//3, i%3]
            box_data = df[metric].dropna()
            bp = ax.boxplot(box_data, patch_artist=True, labels=[title])
            bp['boxes'][0].set_facecolor(self.colors['primary'])
            bp['boxes'][0].set_alpha(0.7)
            ax.set_ylabel('Value', fontsize=10)
            ax.grid(True, alpha=0.3)
            
            # Add statistics
            mean_val = box_data.mean()
            std_val = box_data.std()
            ax.text(0.5, 0.95, f'Mean: {mean_val:.3f}\nStd: {std_val:.3f}', 
                   transform=ax.transAxes, fontsize=9, verticalalignment='top',
                   bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'statistical_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def create_correlation_heatmap(self, df: pd.DataFrame):
        """Create detailed correlation heatmap"""
        # Select numeric columns for correlation
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        correlation_matrix = df[numeric_cols].corr()
        
        plt.figure(figsize=(14, 12))
        mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
        
        # Create heatmap
        sns.heatmap(correlation_matrix, mask=mask, annot=True, cmap='RdBu_r', center=0,
                   square=True, linewidths=0.5, cbar_kws={"shrink": 0.8},
                   fmt='.3f', annot_kws={'size': 10})
        
        plt.title('Behavioral Metrics Correlation Matrix', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.savefig(self.output_dir / 'correlation_heatmap.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def create_time_series_analysis(self, df: pd.DataFrame):
        """Create time series analysis plots"""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Temporal Analysis of Behavioral Metrics', fontsize=16, fontweight='bold')
        
        # Sort by track ID for time series
        df_sorted = df.sort_values('track_id')
        
        # Speed over time
        axes[0, 0].plot(df_sorted['track_id'], df_sorted['average_speed_mm_s'], 
                       alpha=0.7, color=self.colors['primary'], linewidth=1)
        axes[0, 0].set_xlabel('Track ID', fontsize=12)
        axes[0, 0].set_ylabel('Average Speed (mm/s)', fontsize=12)
        axes[0, 0].set_title('Speed Over Time', fontsize=14, fontweight='bold')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Activity level over time
        axes[0, 1].plot(df_sorted['track_id'], df_sorted['activity_level'], 
                       alpha=0.7, color=self.colors['secondary'], linewidth=1)
        axes[0, 1].set_xlabel('Track ID', fontsize=12)
        axes[0, 1].set_ylabel('Activity Level', fontsize=12)
        axes[0, 1].set_title('Activity Level Over Time', fontsize=14, fontweight='bold')
        axes[0, 1].grid(True, alpha=0.3)
        
        # Distance over time
        axes[1, 0].plot(df_sorted['track_id'], df_sorted['total_distance_mm'], 
                       alpha=0.7, color=self.colors['info'], linewidth=1)
        axes[1, 0].set_xlabel('Track ID', fontsize=12)
        axes[1, 0].set_ylabel('Total Distance (mm)', fontsize=12)
        axes[1, 0].set_title('Distance Over Time', fontsize=14, fontweight='bold')
        axes[1, 0].grid(True, alpha=0.3)
        
        # Pose variability over time
        axes[1, 1].plot(df_sorted['track_id'], df_sorted['pose_variability'], 
                       alpha=0.7, color=self.colors['warning'], linewidth=1)
        axes[1, 1].set_xlabel('Track ID', fontsize=12)
        axes[1, 1].set_ylabel('Pose Variability', fontsize=12)
        axes[1, 1].set_title('Pose Variability Over Time', fontsize=14, fontweight='bold')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'time_series_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def create_behavioral_clusters(self, df: pd.DataFrame):
        """Create behavioral clustering analysis"""
        from sklearn.cluster import KMeans
        from sklearn.preprocessing import StandardScaler
        
        # Select features for clustering
        features = ['average_speed_mm_s', 'total_distance_mm', 'activity_level', 
                   'movement_frequency', 'pose_variability', 'turning_frequency']
        X = df[features].fillna(0)
        
        # Standardize features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Perform K-means clustering
        kmeans = KMeans(n_clusters=3, random_state=42)
        clusters = kmeans.fit_predict(X_scaled)
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Behavioral Clustering Analysis', fontsize=16, fontweight='bold')
        
        # Speed vs Distance colored by cluster
        scatter = axes[0, 0].scatter(df['total_distance_mm'], df['average_speed_mm_s'], 
                                   c=clusters, cmap='viridis', alpha=0.7, s=50)
        axes[0, 0].set_xlabel('Total Distance (mm)', fontsize=12)
        axes[0, 0].set_ylabel('Average Speed (mm/s)', fontsize=12)
        axes[0, 0].set_title('Speed vs Distance (Clustered)', fontsize=14, fontweight='bold')
        axes[0, 0].grid(True, alpha=0.3)
        plt.colorbar(scatter, ax=axes[0, 0], label='Cluster')
        
        # Activity vs Movement frequency colored by cluster
        scatter = axes[0, 1].scatter(df['activity_level'], df['movement_frequency'], 
                                   c=clusters, cmap='viridis', alpha=0.7, s=50)
        axes[0, 1].set_xlabel('Activity Level', fontsize=12)
        axes[0, 1].set_ylabel('Movement Frequency', fontsize=12)
        axes[0, 1].set_title('Activity vs Movement Frequency (Clustered)', fontsize=14, fontweight='bold')
        axes[0, 1].grid(True, alpha=0.3)
        plt.colorbar(scatter, ax=axes[0, 1], label='Cluster')
        
        # Cluster distribution
        cluster_counts = pd.Series(clusters).value_counts().sort_index()
        bars = axes[1, 0].bar(cluster_counts.index, cluster_counts.values, 
                             color=[self.colors['primary'], self.colors['secondary'], self.colors['accent']],
                             alpha=0.7, edgecolor='white', linewidth=1)
        axes[1, 0].set_xlabel('Cluster', fontsize=12)
        axes[1, 0].set_ylabel('Number of Tracks', fontsize=12)
        axes[1, 0].set_title('Cluster Distribution', fontsize=14, fontweight='bold')
        axes[1, 0].grid(True, alpha=0.3, axis='y')
        
        # Add value labels
        for bar, v in zip(bars, cluster_counts.values):
            axes[1, 0].text(bar.get_x() + bar.get_width()/2, v + 0.5, f'{v}', 
                           ha='center', va='bottom', fontsize=10)
        
        # Feature importance for clusters
        feature_importance = np.abs(kmeans.cluster_centers_).mean(axis=0)
        bars = axes[1, 1].bar(features, feature_importance, 
                             color=self.colors['info'], alpha=0.7, edgecolor='white', linewidth=1)
        axes[1, 1].set_xlabel('Features', fontsize=12)
        axes[1, 1].set_ylabel('Average Importance', fontsize=12)
        axes[1, 1].set_title('Feature Importance for Clustering', fontsize=14, fontweight='bold')
        axes[1, 1].tick_params(axis='x', rotation=45)
        axes[1, 1].grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'behavioral_clusters.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def create_region_analysis(self, df: pd.DataFrame):
        """Create detailed spatial behavior analysis"""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Spatial Behavior Analysis', fontsize=16, fontweight='bold')
        
        # Region preference pie chart
        region_data = df[['time_in_center', 'time_in_edge', 'time_in_corner']].mean()
        region_colors = [self.colors['info'], self.colors['accent'], self.colors['success']]
        region_labels = ['Center', 'Edge', 'Corner']
        
        wedges, texts, autotexts = axes[0, 0].pie(region_data.values, labels=region_labels, 
                                                 autopct='%1.1f%%', startangle=90, colors=region_colors)
        axes[0, 0].set_title('Average Time Spent in Regions', fontsize=14, fontweight='bold')
        
        # Region preference distribution
        region_preference = df[['time_in_center', 'time_in_edge', 'time_in_corner']].idxmax(axis=1)
        region_counts = region_preference.value_counts()
        
        bars = axes[0, 1].bar(region_counts.index, region_counts.values, 
                             color=region_colors, alpha=0.7, edgecolor='white', linewidth=1)
        axes[0, 1].set_xlabel('Preferred Region', fontsize=12)
        axes[0, 1].set_ylabel('Number of Tracks', fontsize=12)
        axes[0, 1].set_title('Primary Region Preference', fontsize=14, fontweight='bold')
        axes[0, 1].grid(True, alpha=0.3, axis='y')
        
        # Add value labels
        for bar, v in zip(bars, region_counts.values):
            axes[0, 1].text(bar.get_x() + bar.get_width()/2, v + 0.5, f'{v}', 
                           ha='center', va='bottom', fontsize=10)
        
        # Activity level by region
        region_activity = df.groupby(region_preference)['activity_level'].mean()
        bars = axes[1, 0].bar(region_activity.index, region_activity.values, 
                             color=region_colors, alpha=0.7, edgecolor='white', linewidth=1)
        axes[1, 0].set_xlabel('Region', fontsize=12)
        axes[1, 0].set_ylabel('Average Activity Level', fontsize=12)
        axes[1, 0].set_title('Activity Level by Region', fontsize=14, fontweight='bold')
        axes[1, 0].grid(True, alpha=0.3, axis='y')
        
        # Speed by region
        region_speed = df.groupby(region_preference)['average_speed_mm_s'].mean()
        bars = axes[1, 1].bar(region_speed.index, region_speed.values, 
                             color=region_colors, alpha=0.7, edgecolor='white', linewidth=1)
        axes[1, 1].set_xlabel('Region', fontsize=12)
        axes[1, 1].set_ylabel('Average Speed (mm/s)', fontsize=12)
        axes[1, 1].set_title('Speed by Region', fontsize=14, fontweight='bold')
        axes[1, 1].grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'spatial_behavior_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def create_all_research_visualizations(self, metrics_file: str, summary_file: str):
        """Create all research-focused visualizations"""
        print("Loading data...")
        df, summary = self.load_data(metrics_file, summary_file)
        
        print("Creating comprehensive dashboard...")
        self.create_comprehensive_dashboard(df, summary)
        
        print("Creating statistical analysis...")
        self.create_statistical_analysis(df)
        
        print("Creating correlation heatmap...")
        self.create_correlation_heatmap(df)
        
        print("Creating time series analysis...")
        self.create_time_series_analysis(df)
        
        print("Creating behavioral clusters...")
        self.create_behavioral_clusters(df)
        
        print("Creating spatial behavior analysis...")
        self.create_region_analysis(df)
        
        print(f"Research visualizations saved to {self.output_dir}")

def main():
    parser = argparse.ArgumentParser(description='Research-Focused Behavioral Analysis Visualization')
    parser.add_argument('--metrics_file', type=str,
                       default='/mnt/storage5/Fruitfly/Task4_BehavioralAnalysis/results/behavioral_metrics_detailed.csv',
                       help='Path to detailed metrics CSV file')
    parser.add_argument('--summary_file', type=str,
                       default='/mnt/storage5/Fruitfly/Task4_BehavioralAnalysis/results/behavioral_summary.json',
                       help='Path to summary JSON file')
    parser.add_argument('--output_dir', type=str,
                       default='/mnt/storage5/Fruitfly/Task4_BehavioralAnalysis/visualizations',
                       help='Output directory for visualizations')
    
    args = parser.parse_args()
    
    print("Starting Research-Focused Behavioral Analysis Visualization...")
    print(f"Metrics file: {args.metrics_file}")
    print(f"Summary file: {args.summary_file}")
    print(f"Output directory: {args.output_dir}")
    
    visualizer = ResearchBehavioralVisualizer(args.output_dir)
    visualizer.create_all_research_visualizations(args.metrics_file, args.summary_file)
    
    print("Research visualization complete!")

if __name__ == "__main__":
    main()


