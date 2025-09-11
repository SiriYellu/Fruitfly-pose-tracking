#!/usr/bin/env python3
"""
Behavioral Analysis Visualization for Task 4
Creates comprehensive visualizations of behavioral metrics
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

class BehavioralVisualizer:
    """Creates visualizations for behavioral analysis results"""
    
    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Set radium-inspired color palette
        self.colors = {
            'primary': '#00FF41',      # Bright radium green
            'secondary': '#00E6FF',    # Cyan blue
            'accent': '#FF6B00',       # Orange
            'warning': '#FFD700',      # Gold
            'danger': '#FF1744',       # Red
            'info': '#3F51B5',         # Indigo
            'success': '#4CAF50',      # Green
            'dark': '#1A1A1A',         # Dark background
            'light': '#F5F5F5',        # Light background
            'text': '#FFFFFF',         # White text
            'text_dark': '#333333'     # Dark text
        }
        
        # Set modern style
        plt.style.use('dark_background')
        sns.set_palette([self.colors['primary'], self.colors['secondary'], 
                        self.colors['accent'], self.colors['warning']])
        
        # Set global font settings
        plt.rcParams.update({
            'font.size': 12,
            'font.weight': 'bold',
            'axes.labelcolor': self.colors['text'],
            'text.color': self.colors['text'],
            'axes.edgecolor': self.colors['primary'],
            'axes.linewidth': 2,
            'grid.color': self.colors['primary'],
            'grid.alpha': 0.3
        })
        
    def load_data(self, metrics_file: str, summary_file: str) -> Tuple[pd.DataFrame, Dict]:
        """Load behavioral metrics and summary data"""
        metrics_df = pd.read_csv(metrics_file)
        
        with open(summary_file, 'r') as f:
            summary = json.load(f)
        
        return metrics_df, summary
    
    def create_speed_analysis(self, df: pd.DataFrame):
        """Create speed analysis visualizations with radium palette"""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.patch.set_facecolor(self.colors['dark'])
        fig.suptitle('🚀 SPEED ANALYSIS - Fruit Fly Movement Patterns', 
                    fontsize=20, fontweight='bold', color=self.colors['primary'], y=0.95)
        
        # Average speed distribution with glow effect
        n, bins, patches = axes[0, 0].hist(df['average_speed_mm_s'], bins=30, alpha=0.8, 
                                          color=self.colors['primary'], edgecolor=self.colors['secondary'], 
                                          linewidth=2)
        axes[0, 0].set_xlabel('Average Speed (mm/s)', fontsize=14, color=self.colors['text'])
        axes[0, 0].set_ylabel('Frequency', fontsize=14, color=self.colors['text'])
        axes[0, 0].set_title('📊 Distribution of Average Speed', fontsize=16, color=self.colors['secondary'])
        axes[0, 0].axvline(df['average_speed_mm_s'].mean(), color=self.colors['warning'], 
                          linestyle='--', linewidth=3, 
                          label=f'Mean: {df["average_speed_mm_s"].mean():.2f} mm/s')
        axes[0, 0].legend(fontsize=12, framealpha=0.8)
        axes[0, 0].grid(True, alpha=0.3, color=self.colors['primary'])
        
        # Max speed distribution
        n, bins, patches = axes[0, 1].hist(df['max_speed_mm_s'], bins=30, alpha=0.8, 
                                          color=self.colors['accent'], edgecolor=self.colors['warning'], 
                                          linewidth=2)
        axes[0, 1].set_xlabel('Max Speed (mm/s)', fontsize=14, color=self.colors['text'])
        axes[0, 1].set_ylabel('Frequency', fontsize=14, color=self.colors['text'])
        axes[0, 1].set_title('⚡ Distribution of Max Speed', fontsize=16, color=self.colors['warning'])
        axes[0, 1].axvline(df['max_speed_mm_s'].mean(), color=self.colors['danger'], 
                          linestyle='--', linewidth=3,
                          label=f'Mean: {df["max_speed_mm_s"].mean():.2f} mm/s')
        axes[0, 1].legend(fontsize=12, framealpha=0.8)
        axes[0, 1].grid(True, alpha=0.3, color=self.colors['primary'])
        
        # Speed vs Distance with gradient effect
        scatter = axes[1, 0].scatter(df['total_distance_mm'], df['average_speed_mm_s'], 
                                   alpha=0.7, c=df['activity_level'], 
                                   cmap='viridis', s=60, edgecolors=self.colors['primary'], linewidth=1)
        axes[1, 0].set_xlabel('Total Distance (mm)', fontsize=14, color=self.colors['text'])
        axes[1, 0].set_ylabel('Average Speed (mm/s)', fontsize=14, color=self.colors['text'])
        axes[1, 0].set_title('🎯 Speed vs Distance Relationship', fontsize=16, color=self.colors['info'])
        axes[1, 0].grid(True, alpha=0.3, color=self.colors['primary'])
        cbar = plt.colorbar(scatter, ax=axes[1, 0])
        cbar.set_label('Activity Level', color=self.colors['text'])
        
        # Speed vs Activity Level
        axes[1, 1].scatter(df['activity_level'], df['average_speed_mm_s'], alpha=0.7, 
                          color=self.colors['secondary'], s=60, edgecolors=self.colors['primary'], linewidth=1)
        axes[1, 1].set_xlabel('Activity Level', fontsize=14, color=self.colors['text'])
        axes[1, 1].set_ylabel('Average Speed (mm/s)', fontsize=14, color=self.colors['text'])
        axes[1, 1].set_title('💫 Speed vs Activity Level', fontsize=16, color=self.colors['success'])
        axes[1, 1].grid(True, alpha=0.3, color=self.colors['primary'])
        
        # Add correlation coefficient
        corr = df['activity_level'].corr(df['average_speed_mm_s'])
        axes[1, 1].text(0.05, 0.95, f'Correlation: {corr:.3f}', 
                       transform=axes[1, 1].transAxes, fontsize=12, 
                       bbox=dict(boxstyle="round,pad=0.3", facecolor=self.colors['dark'], 
                               edgecolor=self.colors['primary'], alpha=0.8),
                       color=self.colors['text'])
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'speed_analysis.png', dpi=300, bbox_inches='tight', 
                   facecolor=self.colors['dark'], edgecolor='none')
        plt.close()
    
    def create_movement_analysis(self, df: pd.DataFrame):
        """Create movement pattern analysis visualizations with radium palette"""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.patch.set_facecolor(self.colors['dark'])
        fig.suptitle('🏃 MOVEMENT PATTERN ANALYSIS - Activity & Behavior', 
                    fontsize=20, fontweight='bold', color=self.colors['primary'], y=0.95)
        
        # Activity level distribution with gradient
        n, bins, patches = axes[0, 0].hist(df['activity_level'], bins=30, alpha=0.8, 
                                          color=self.colors['accent'], edgecolor=self.colors['warning'], 
                                          linewidth=2)
        axes[0, 0].set_xlabel('Activity Level (0-1)', fontsize=14, color=self.colors['text'])
        axes[0, 0].set_ylabel('Frequency', fontsize=14, color=self.colors['text'])
        axes[0, 0].set_title('🎯 Distribution of Activity Level', fontsize=16, color=self.colors['warning'])
        axes[0, 0].axvline(df['activity_level'].mean(), color=self.colors['danger'], 
                          linestyle='--', linewidth=3,
                          label=f'Mean: {df["activity_level"].mean():.3f}')
        axes[0, 0].legend(fontsize=12, framealpha=0.8)
        axes[0, 0].grid(True, alpha=0.3, color=self.colors['primary'])
        
        # Movement frequency distribution
        n, bins, patches = axes[0, 1].hist(df['movement_frequency'], bins=30, alpha=0.8, 
                                          color=self.colors['secondary'], edgecolor=self.colors['info'], 
                                          linewidth=2)
        axes[0, 1].set_xlabel('Movement Frequency (bouts)', fontsize=14, color=self.colors['text'])
        axes[0, 1].set_ylabel('Frequency', fontsize=14, color=self.colors['text'])
        axes[0, 1].set_title('🔄 Distribution of Movement Frequency', fontsize=16, color=self.colors['info'])
        axes[0, 1].axvline(df['movement_frequency'].mean(), color=self.colors['danger'], 
                          linestyle='--', linewidth=3,
                          label=f'Mean: {df["movement_frequency"].mean():.1f}')
        axes[0, 1].legend(fontsize=12, framealpha=0.8)
        axes[0, 1].grid(True, alpha=0.3, color=self.colors['primary'])
        
        # Stationary duration distribution
        n, bins, patches = axes[1, 0].hist(df['stationary_duration_s'], bins=30, alpha=0.8, 
                                          color=self.colors['success'], edgecolor=self.colors['primary'], 
                                          linewidth=2)
        axes[1, 0].set_xlabel('Stationary Duration (seconds)', fontsize=14, color=self.colors['text'])
        axes[1, 0].set_ylabel('Frequency', fontsize=14, color=self.colors['text'])
        axes[1, 0].set_title('⏸️ Distribution of Stationary Duration', fontsize=16, color=self.colors['success'])
        axes[1, 0].axvline(df['stationary_duration_s'].mean(), color=self.colors['warning'], 
                          linestyle='--', linewidth=3,
                          label=f'Mean: {df["stationary_duration_s"].mean():.2f}s')
        axes[1, 0].legend(fontsize=12, framealpha=0.8)
        axes[1, 0].grid(True, alpha=0.3, color=self.colors['primary'])
        
        # Activity vs Movement Frequency with trend line
        scatter = axes[1, 1].scatter(df['activity_level'], df['movement_frequency'], alpha=0.7, 
                                   color=self.colors['primary'], s=60, edgecolors=self.colors['secondary'], 
                                   linewidth=1)
        axes[1, 1].set_xlabel('Activity Level', fontsize=14, color=self.colors['text'])
        axes[1, 1].set_ylabel('Movement Frequency', fontsize=14, color=self.colors['text'])
        axes[1, 1].set_title('💫 Activity Level vs Movement Frequency', fontsize=16, color=self.colors['accent'])
        axes[1, 1].grid(True, alpha=0.3, color=self.colors['primary'])
        
        # Add trend line
        z = np.polyfit(df['activity_level'], df['movement_frequency'], 1)
        p = np.poly1d(z)
        axes[1, 1].plot(df['activity_level'], p(df['activity_level']), 
                       color=self.colors['warning'], linestyle='--', linewidth=2, alpha=0.8)
        
        # Add correlation coefficient
        corr = df['activity_level'].corr(df['movement_frequency'])
        axes[1, 1].text(0.05, 0.95, f'Correlation: {corr:.3f}', 
                       transform=axes[1, 1].transAxes, fontsize=12, 
                       bbox=dict(boxstyle="round,pad=0.3", facecolor=self.colors['dark'], 
                               edgecolor=self.colors['primary'], alpha=0.8),
                       color=self.colors['text'])
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'movement_analysis.png', dpi=300, bbox_inches='tight', 
                   facecolor=self.colors['dark'], edgecolor='none')
        plt.close()
    
    def create_region_analysis(self, df: pd.DataFrame):
        """Create region occupancy analysis visualizations with radium palette"""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.patch.set_facecolor(self.colors['dark'])
        fig.suptitle('🗺️ SPATIAL BEHAVIOR ANALYSIS - Region Occupancy Patterns', 
                    fontsize=20, fontweight='bold', color=self.colors['primary'], y=0.95)
        
        # Time in different regions with enhanced bars
        region_data = df[['time_in_center', 'time_in_edge', 'time_in_corner']].mean()
        region_colors = [self.colors['success'], self.colors['accent'], self.colors['danger']]
        region_labels = ['Center', 'Edge', 'Corner']
        
        bars = axes[0, 0].bar(region_labels, region_data.values, color=region_colors, alpha=0.8, 
                             edgecolor=self.colors['primary'], linewidth=2)
        axes[0, 0].set_ylabel('Average Time Proportion', fontsize=14, color=self.colors['text'])
        axes[0, 0].set_title('📍 Average Time Spent in Different Regions', fontsize=16, color=self.colors['secondary'])
        axes[0, 0].set_ylim(0, 1)
        axes[0, 0].grid(True, alpha=0.3, color=self.colors['primary'], axis='y')
        
        # Add value labels on bars with glow effect
        for i, (bar, v) in enumerate(zip(bars, region_data.values)):
            axes[0, 0].text(bar.get_x() + bar.get_width()/2, v + 0.02, f'{v:.3f}', 
                           ha='center', va='bottom', fontsize=12, fontweight='bold',
                           color=self.colors['text'], 
                           bbox=dict(boxstyle="round,pad=0.2", facecolor=self.colors['dark'], 
                                   edgecolor=region_colors[i], alpha=0.8))
        
        # Region preference distribution with enhanced pie chart
        region_preference = df[['time_in_center', 'time_in_edge', 'time_in_corner']].idxmax(axis=1)
        region_counts = region_preference.value_counts()
        
        wedges, texts, autotexts = axes[0, 1].pie(region_counts.values, labels=region_counts.index, 
                                                 autopct='%1.1f%%', startangle=90, colors=region_colors,
                                                 explode=[0.05, 0.05, 0.05], shadow=True, alpha=0.8)
        axes[0, 1].set_title('🎯 Primary Region Preference Distribution', fontsize=16, color=self.colors['warning'])
        
        # Enhance pie chart text
        for autotext in autotexts:
            autotext.set_color(self.colors['text'])
            autotext.set_fontsize(12)
            autotext.set_fontweight('bold')
        
        # Center vs Edge time with trend line
        scatter = axes[1, 0].scatter(df['time_in_center'], df['time_in_edge'], alpha=0.7, 
                                   color=self.colors['primary'], s=60, edgecolors=self.colors['secondary'], 
                                   linewidth=1)
        axes[1, 0].set_xlabel('Time in Center', fontsize=14, color=self.colors['text'])
        axes[1, 0].set_ylabel('Time in Edge', fontsize=14, color=self.colors['text'])
        axes[1, 0].set_title('🔄 Center vs Edge Time Relationship', fontsize=16, color=self.colors['info'])
        axes[1, 0].grid(True, alpha=0.3, color=self.colors['primary'])
        
        # Add trend line
        z = np.polyfit(df['time_in_center'], df['time_in_edge'], 1)
        p = np.poly1d(z)
        axes[1, 0].plot(df['time_in_center'], p(df['time_in_center']), 
                       color=self.colors['warning'], linestyle='--', linewidth=2, alpha=0.8)
        
        # Region time vs Activity with enhanced scatter
        scatter1 = axes[1, 1].scatter(df['time_in_center'], df['activity_level'], alpha=0.7, 
                                    color=self.colors['success'], s=60, edgecolors=self.colors['primary'], 
                                    linewidth=1, label='Center')
        scatter2 = axes[1, 1].scatter(df['time_in_edge'], df['activity_level'], alpha=0.7, 
                                    color=self.colors['accent'], s=60, edgecolors=self.colors['primary'], 
                                    linewidth=1, label='Edge')
        scatter3 = axes[1, 1].scatter(df['time_in_corner'], df['activity_level'], alpha=0.7, 
                                    color=self.colors['danger'], s=60, edgecolors=self.colors['primary'], 
                                    linewidth=1, label='Corner')
        
        axes[1, 1].set_xlabel('Time in Region', fontsize=14, color=self.colors['text'])
        axes[1, 1].set_ylabel('Activity Level', fontsize=14, color=self.colors['text'])
        axes[1, 1].set_title('💫 Region Time vs Activity Level', fontsize=16, color=self.colors['accent'])
        axes[1, 1].legend(fontsize=12, framealpha=0.8)
        axes[1, 1].grid(True, alpha=0.3, color=self.colors['primary'])
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'region_analysis.png', dpi=300, bbox_inches='tight', 
                   facecolor=self.colors['dark'], edgecolor='none')
        plt.close()
    
    def create_pose_analysis(self, df: pd.DataFrame):
        """Create pose variability analysis visualizations"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Pose Variability Analysis', fontsize=16, fontweight='bold')
        
        # Pose variability distribution
        axes[0, 0].hist(df['pose_variability'], bins=30, alpha=0.7, color='indigo', edgecolor='black')
        axes[0, 0].set_xlabel('Pose Variability')
        axes[0, 0].set_ylabel('Frequency')
        axes[0, 0].set_title('Distribution of Pose Variability')
        axes[0, 0].axvline(df['pose_variability'].mean(), color='red', linestyle='--',
                          label=f'Mean: {df["pose_variability"].mean():.2f}')
        axes[0, 0].legend()
        
        # Turning frequency distribution
        axes[0, 1].hist(df['turning_frequency'], bins=30, alpha=0.7, color='crimson', edgecolor='black')
        axes[0, 1].set_xlabel('Turning Frequency')
        axes[0, 1].set_ylabel('Frequency')
        axes[0, 1].set_title('Distribution of Turning Frequency')
        axes[0, 1].axvline(df['turning_frequency'].mean(), color='red', linestyle='--',
                          label=f'Mean: {df["turning_frequency"].mean():.2f}')
        axes[0, 1].legend()
        
        # Pose variability vs Activity
        axes[1, 0].scatter(df['pose_variability'], df['activity_level'], alpha=0.6, color='darkgreen')
        axes[1, 0].set_xlabel('Pose Variability')
        axes[1, 0].set_ylabel('Activity Level')
        axes[1, 0].set_title('Pose Variability vs Activity Level')
        
        # Turning frequency vs Speed
        axes[1, 1].scatter(df['turning_frequency'], df['average_speed_mm_s'], alpha=0.6, color='darkblue')
        axes[1, 1].set_xlabel('Turning Frequency')
        axes[1, 1].set_ylabel('Average Speed (mm/s)')
        axes[1, 1].set_title('Turning Frequency vs Speed')
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'pose_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def create_correlation_matrix(self, df: pd.DataFrame):
        """Create correlation matrix heatmap"""
        # Select numeric columns for correlation
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        correlation_matrix = df[numeric_cols].corr()
        
        plt.figure(figsize=(12, 10))
        mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
        sns.heatmap(correlation_matrix, mask=mask, annot=True, cmap='coolwarm', center=0,
                   square=True, linewidths=0.5, cbar_kws={"shrink": 0.8})
        plt.title('Behavioral Metrics Correlation Matrix', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.savefig(self.output_dir / 'correlation_matrix.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def create_summary_dashboard(self, df: pd.DataFrame, summary: Dict):
        """Create a comprehensive summary dashboard"""
        fig = plt.figure(figsize=(20, 16))
        gs = fig.add_gridspec(4, 4, hspace=0.3, wspace=0.3)
        
        # Title
        fig.suptitle('Fruit Fly Behavioral Analysis Dashboard', fontsize=20, fontweight='bold', y=0.95)
        
        # Key statistics
        ax1 = fig.add_subplot(gs[0, :2])
        ax1.axis('off')
        stats_text = f"""
        Key Statistics:
        • Total Tracks Analyzed: {summary['total_tracks']}
        • Average Distance: {summary['total_distance_mean']:.2f} ± {summary['total_distance_std']:.2f} mm
        • Average Speed: {summary['average_speed_mean']:.2f} ± {summary['average_speed_std']:.2f} mm/s
        • Activity Level: {summary['activity_level_mean']:.2f} ± {summary['activity_level_std']:.2f}
        • Movement Frequency: {summary['movement_frequency_mean']:.2f} ± {summary['movement_frequency_std']:.2f}
        • Time in Center: {summary['time_in_center_mean']:.2f} ± {summary['time_in_center_std']:.2f}
        """
        ax1.text(0.1, 0.5, stats_text, fontsize=12, verticalalignment='center',
                bbox=dict(boxstyle="round,pad=0.5", facecolor="lightblue", alpha=0.8))
        
        # Speed distribution
        ax2 = fig.add_subplot(gs[0, 2:])
        ax2.hist(df['average_speed_mm_s'], bins=20, alpha=0.7, color='skyblue', edgecolor='black')
        ax2.set_xlabel('Average Speed (mm/s)')
        ax2.set_ylabel('Frequency')
        ax2.set_title('Speed Distribution')
        
        # Activity level
        ax3 = fig.add_subplot(gs[1, :2])
        ax3.hist(df['activity_level'], bins=20, alpha=0.7, color='orange', edgecolor='black')
        ax3.set_xlabel('Activity Level')
        ax3.set_ylabel('Frequency')
        ax3.set_title('Activity Level Distribution')
        
        # Region occupancy
        ax4 = fig.add_subplot(gs[1, 2:])
        region_data = df[['time_in_center', 'time_in_edge', 'time_in_corner']].mean()
        ax4.bar(region_data.index, region_data.values, color=['green', 'orange', 'red'], alpha=0.7)
        ax4.set_ylabel('Average Time Proportion')
        ax4.set_title('Region Occupancy')
        
        # Distance vs Speed
        ax5 = fig.add_subplot(gs[2, :2])
        ax5.scatter(df['total_distance_mm'], df['average_speed_mm_s'], alpha=0.6, color='green')
        ax5.set_xlabel('Total Distance (mm)')
        ax5.set_ylabel('Average Speed (mm/s)')
        ax5.set_title('Distance vs Speed')
        
        # Pose variability
        ax6 = fig.add_subplot(gs[2, 2:])
        ax6.hist(df['pose_variability'], bins=20, alpha=0.7, color='purple', edgecolor='black')
        ax6.set_xlabel('Pose Variability')
        ax6.set_ylabel('Frequency')
        ax6.set_title('Pose Variability Distribution')
        
        # Movement frequency
        ax7 = fig.add_subplot(gs[3, :2])
        ax7.hist(df['movement_frequency'], bins=20, alpha=0.7, color='teal', edgecolor='black')
        ax7.set_xlabel('Movement Frequency')
        ax7.set_ylabel('Frequency')
        ax7.set_title('Movement Frequency Distribution')
        
        # Turning frequency
        ax8 = fig.add_subplot(gs[3, 2:])
        ax8.hist(df['turning_frequency'], bins=20, alpha=0.7, color='crimson', edgecolor='black')
        ax8.set_xlabel('Turning Frequency')
        ax8.set_ylabel('Frequency')
        ax8.set_title('Turning Frequency Distribution')
        
        plt.savefig(self.output_dir / 'behavioral_dashboard.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def create_all_visualizations(self, metrics_file: str, summary_file: str):
        """Create all behavioral analysis visualizations"""
        print("Loading data...")
        df, summary = self.load_data(metrics_file, summary_file)
        
        print("Creating speed analysis...")
        self.create_speed_analysis(df)
        
        print("Creating movement analysis...")
        self.create_movement_analysis(df)
        
        print("Creating region analysis...")
        self.create_region_analysis(df)
        
        print("Creating pose analysis...")
        self.create_pose_analysis(df)
        
        print("Creating correlation matrix...")
        self.create_correlation_matrix(df)
        
        print("Creating summary dashboard...")
        self.create_summary_dashboard(df, summary)
        
        print(f"All visualizations saved to {self.output_dir}")

def main():
    parser = argparse.ArgumentParser(description='Behavioral Analysis Visualization')
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
    
    print("Starting Behavioral Analysis Visualization...")
    print(f"Metrics file: {args.metrics_file}")
    print(f"Summary file: {args.summary_file}")
    print(f"Output directory: {args.output_dir}")
    
    visualizer = BehavioralVisualizer(args.output_dir)
    visualizer.create_all_visualizations(args.metrics_file, args.summary_file)
    
    print("Visualization complete!")

if __name__ == "__main__":
    main()
