#!/usr/bin/env python3
"""
Enhanced Behavioral Analysis Visualization with Radium Palette
Creates stunning, visually appealing visualizations for behavioral analysis results
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

class EnhancedBehavioralVisualizer:
    """Creates enhanced visualizations for behavioral analysis results with radium palette"""
    
    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Enhanced radium-inspired color palette
        self.colors = {
            'primary': '#00FF41',      # Bright radium green
            'secondary': '#00E6FF',    # Cyan blue
            'accent': '#FF6B00',       # Orange
            'warning': '#FFD700',      # Gold
            'danger': '#FF1744',       # Red
            'info': '#3F51B5',         # Indigo
            'success': '#4CAF50',      # Green
            'purple': '#9C27B0',       # Purple
            'dark': '#0A0A0A',         # Very dark background
            'light': '#F5F5F5',        # Light background
            'text': '#FFFFFF',         # White text
            'text_dark': '#333333',    # Dark text
            'glow': '#00FF88'          # Glow effect
        }
        
        # Set enhanced style
        plt.style.use('dark_background')
        sns.set_palette([self.colors['primary'], self.colors['secondary'], 
                        self.colors['accent'], self.colors['warning']])
        
        # Enhanced font settings
        plt.rcParams.update({
            'font.size': 14,
            'font.weight': 'bold',
            'axes.labelcolor': self.colors['text'],
            'text.color': self.colors['text'],
            'axes.edgecolor': self.colors['primary'],
            'axes.linewidth': 3,
            'grid.color': self.colors['primary'],
            'grid.alpha': 0.4,
            'figure.facecolor': self.colors['dark'],
            'axes.facecolor': self.colors['dark'],
            'savefig.facecolor': self.colors['dark'],
            'savefig.edgecolor': 'none'
        })
        
    def load_data(self, metrics_file: str, summary_file: str) -> Tuple[pd.DataFrame, Dict]:
        """Load behavioral metrics and summary data"""
        metrics_df = pd.read_csv(metrics_file)
        
        with open(summary_file, 'r') as f:
            summary = json.load(f)
        
        return metrics_df, summary
    
    def create_enhanced_dashboard(self, df: pd.DataFrame, summary: Dict):
        """Create a stunning comprehensive dashboard"""
        fig = plt.figure(figsize=(24, 18))
        fig.patch.set_facecolor(self.colors['dark'])
        gs = fig.add_gridspec(4, 4, hspace=0.4, wspace=0.3)
        
        # Main title with glow effect
        fig.suptitle('🧬 FRUIT FLY BEHAVIORAL ANALYSIS DASHBOARD 🧬', 
                    fontsize=28, fontweight='bold', color=self.colors['primary'], y=0.96)
        
        # Add subtitle
        fig.text(0.5, 0.92, 'Comprehensive Analysis of Movement Patterns, Spatial Behavior & Pose Dynamics', 
                fontsize=16, ha='center', color=self.colors['secondary'], style='italic')
        
        # Key statistics panel with glow effect
        ax1 = fig.add_subplot(gs[0, :2])
        ax1.axis('off')
        
        # Create glowing background
        rect = Rectangle((0.05, 0.1), 0.9, 0.8, facecolor=self.colors['dark'], 
                        edgecolor=self.colors['primary'], linewidth=3, alpha=0.9)
        ax1.add_patch(rect)
        
        stats_text = f"""
        📊 KEY BEHAVIORAL STATISTICS
        ═══════════════════════════════════════════════════════════════
        
        🎯 Total Tracks Analyzed: {summary['total_tracks']:,}
        📏 Average Distance: {summary['total_distance_mean']:.3f} ± {summary['total_distance_std']:.3f} mm
        🚀 Average Speed: {summary['average_speed_mean']:.3f} ± {summary['average_speed_std']:.3f} mm/s
        ⚡ Max Speed: {summary['max_speed_mean']:.3f} ± {summary['max_speed_std']:.3f} mm/s
        🏃 Activity Level: {summary['activity_level_mean']:.3f} ± {summary['activity_level_std']:.3f}
        🔄 Movement Frequency: {summary['movement_frequency_mean']:.1f} ± {summary['movement_frequency_std']:.1f}
        ⏸️ Stationary Duration: {summary['stationary_duration_mean']:.2f} ± {summary['stationary_duration_std']:.2f} s
        🎭 Pose Variability: {summary['pose_variability_mean']:.3f} ± {summary['pose_variability_std']:.3f}
        """
        
        ax1.text(0.1, 0.5, stats_text, fontsize=14, verticalalignment='center',
                color=self.colors['text'], fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.5", facecolor=self.colors['dark'], 
                         edgecolor=self.colors['primary'], alpha=0.8, linewidth=2))
        
        # Speed distribution with enhanced styling
        ax2 = fig.add_subplot(gs[0, 2:])
        n, bins, patches = ax2.hist(df['average_speed_mm_s'], bins=25, alpha=0.8, 
                                   color=self.colors['primary'], edgecolor=self.colors['secondary'], 
                                   linewidth=2)
        ax2.set_xlabel('Average Speed (mm/s)', fontsize=16, color=self.colors['text'])
        ax2.set_ylabel('Frequency', fontsize=16, color=self.colors['text'])
        ax2.set_title('🚀 Speed Distribution Analysis', fontsize=18, color=self.colors['secondary'])
        ax2.axvline(df['average_speed_mm_s'].mean(), color=self.colors['warning'], 
                   linestyle='--', linewidth=4, label=f'Mean: {df["average_speed_mm_s"].mean():.3f}')
        ax2.legend(fontsize=14, framealpha=0.9)
        ax2.grid(True, alpha=0.4, color=self.colors['primary'])
        
        # Activity level analysis
        ax3 = fig.add_subplot(gs[1, :2])
        n, bins, patches = ax3.hist(df['activity_level'], bins=25, alpha=0.8, 
                                   color=self.colors['accent'], edgecolor=self.colors['warning'], 
                                   linewidth=2)
        ax3.set_xlabel('Activity Level (0-1)', fontsize=16, color=self.colors['text'])
        ax3.set_ylabel('Frequency', fontsize=16, color=self.colors['text'])
        ax3.set_title('🎯 Activity Level Distribution', fontsize=18, color=self.colors['warning'])
        ax3.axvline(df['activity_level'].mean(), color=self.colors['danger'], 
                   linestyle='--', linewidth=4, label=f'Mean: {df["activity_level"].mean():.3f}')
        ax3.legend(fontsize=14, framealpha=0.9)
        ax3.grid(True, alpha=0.4, color=self.colors['primary'])
        
        # Region occupancy with enhanced pie chart
        ax4 = fig.add_subplot(gs[1, 2:])
        region_data = df[['time_in_center', 'time_in_edge', 'time_in_corner']].mean()
        region_colors = [self.colors['success'], self.colors['accent'], self.colors['danger']]
        region_labels = ['Center', 'Edge', 'Corner']
        
        wedges, texts, autotexts = ax4.pie(region_data.values, labels=region_labels, 
                                          autopct='%1.1f%%', startangle=90, colors=region_colors,
                                          explode=[0.1, 0.05, 0.05], shadow=True)
        ax4.set_title('🗺️ Spatial Behavior - Region Occupancy', fontsize=18, color=self.colors['info'])
        
        # Enhance pie chart text
        for autotext in autotexts:
            autotext.set_color(self.colors['text'])
            autotext.set_fontsize(14)
            autotext.set_fontweight('bold')
        
        # Speed vs Distance with enhanced scatter
        ax5 = fig.add_subplot(gs[2, :2])
        scatter = ax5.scatter(df['total_distance_mm'], df['average_speed_mm_s'], 
                            alpha=0.7, c=df['activity_level'], cmap='viridis', 
                            s=80, edgecolors=self.colors['primary'], linewidth=2)
        ax5.set_xlabel('Total Distance (mm)', fontsize=16, color=self.colors['text'])
        ax5.set_ylabel('Average Speed (mm/s)', fontsize=16, color=self.colors['text'])
        ax5.set_title('🎯 Speed vs Distance Relationship', fontsize=18, color=self.colors['info'])
        ax5.grid(True, alpha=0.4, color=self.colors['primary'])
        
        # Add colorbar
        cbar = plt.colorbar(scatter, ax=ax5)
        cbar.set_label('Activity Level', fontsize=14, color=self.colors['text'])
        cbar.ax.tick_params(colors=self.colors['text'])
        
        # Pose variability analysis
        ax6 = fig.add_subplot(gs[2, 2:])
        n, bins, patches = ax6.hist(df['pose_variability'], bins=25, alpha=0.8, 
                                   color=self.colors['purple'], edgecolor=self.colors['primary'], 
                                   linewidth=2)
        ax6.set_xlabel('Pose Variability', fontsize=16, color=self.colors['text'])
        ax6.set_ylabel('Frequency', fontsize=16, color=self.colors['text'])
        ax6.set_title('🎭 Pose Variability Distribution', fontsize=18, color=self.colors['purple'])
        ax6.axvline(df['pose_variability'].mean(), color=self.colors['warning'], 
                   linestyle='--', linewidth=4, label=f'Mean: {df["pose_variability"].mean():.3f}')
        ax6.legend(fontsize=14, framealpha=0.9)
        ax6.grid(True, alpha=0.4, color=self.colors['primary'])
        
        # Movement frequency analysis
        ax7 = fig.add_subplot(gs[3, :2])
        n, bins, patches = ax7.hist(df['movement_frequency'], bins=25, alpha=0.8, 
                                   color=self.colors['secondary'], edgecolor=self.colors['info'], 
                                   linewidth=2)
        ax7.set_xlabel('Movement Frequency (bouts)', fontsize=16, color=self.colors['text'])
        ax7.set_ylabel('Frequency', fontsize=16, color=self.colors['text'])
        ax7.set_title('🔄 Movement Frequency Distribution', fontsize=18, color=self.colors['info'])
        ax7.axvline(df['movement_frequency'].mean(), color=self.colors['danger'], 
                   linestyle='--', linewidth=4, label=f'Mean: {df["movement_frequency"].mean():.1f}')
        ax7.legend(fontsize=14, framealpha=0.9)
        ax7.grid(True, alpha=0.4, color=self.colors['primary'])
        
        # Activity vs Region time
        ax8 = fig.add_subplot(gs[3, 2:])
        scatter1 = ax8.scatter(df['time_in_center'], df['activity_level'], alpha=0.7, 
                             color=self.colors['success'], s=60, edgecolors=self.colors['primary'], 
                             linewidth=1, label='Center')
        scatter2 = ax8.scatter(df['time_in_edge'], df['activity_level'], alpha=0.7, 
                             color=self.colors['accent'], s=60, edgecolors=self.colors['primary'], 
                             linewidth=1, label='Edge')
        scatter3 = ax8.scatter(df['time_in_corner'], df['activity_level'], alpha=0.7, 
                             color=self.colors['danger'], s=60, edgecolors=self.colors['primary'], 
                             linewidth=1, label='Corner')
        
        ax8.set_xlabel('Time in Region', fontsize=16, color=self.colors['text'])
        ax8.set_ylabel('Activity Level', fontsize=16, color=self.colors['text'])
        ax8.set_title('💫 Region Time vs Activity Level', fontsize=18, color=self.colors['accent'])
        ax8.legend(fontsize=14, framealpha=0.9)
        ax8.grid(True, alpha=0.4, color=self.colors['primary'])
        
        # Add footer
        fig.text(0.5, 0.02, 'Generated by Enhanced Behavioral Analysis System | Radium Color Palette', 
                fontsize=12, ha='center', color=self.colors['secondary'], style='italic')
        
        plt.savefig(self.output_dir / 'enhanced_behavioral_dashboard.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def create_radium_speed_analysis(self, df: pd.DataFrame):
        """Create stunning speed analysis with radium effects"""
        fig, axes = plt.subplots(2, 2, figsize=(20, 16))
        fig.patch.set_facecolor(self.colors['dark'])
        fig.suptitle('🚀 RADIUM SPEED ANALYSIS - Fruit Fly Movement Dynamics', 
                    fontsize=24, fontweight='bold', color=self.colors['primary'], y=0.95)
        
        # Average speed distribution with glow effect
        n, bins, patches = axes[0, 0].hist(df['average_speed_mm_s'], bins=40, alpha=0.9, 
                                          color=self.colors['primary'], edgecolor=self.colors['secondary'], 
                                          linewidth=3)
        axes[0, 0].set_xlabel('Average Speed (mm/s)', fontsize=18, color=self.colors['text'])
        axes[0, 0].set_ylabel('Frequency', fontsize=18, color=self.colors['text'])
        axes[0, 0].set_title('📊 Distribution of Average Speed', fontsize=20, color=self.colors['secondary'])
        axes[0, 0].axvline(df['average_speed_mm_s'].mean(), color=self.colors['warning'], 
                          linestyle='--', linewidth=5, 
                          label=f'Mean: {df["average_speed_mm_s"].mean():.3f} mm/s')
        axes[0, 0].legend(fontsize=16, framealpha=0.9)
        axes[0, 0].grid(True, alpha=0.4, color=self.colors['primary'])
        
        # Max speed distribution
        n, bins, patches = axes[0, 1].hist(df['max_speed_mm_s'], bins=40, alpha=0.9, 
                                          color=self.colors['accent'], edgecolor=self.colors['warning'], 
                                          linewidth=3)
        axes[0, 1].set_xlabel('Max Speed (mm/s)', fontsize=18, color=self.colors['text'])
        axes[0, 1].set_ylabel('Frequency', fontsize=18, color=self.colors['text'])
        axes[0, 1].set_title('⚡ Distribution of Max Speed', fontsize=20, color=self.colors['warning'])
        axes[0, 1].axvline(df['max_speed_mm_s'].mean(), color=self.colors['danger'], 
                          linestyle='--', linewidth=5,
                          label=f'Mean: {df["max_speed_mm_s"].mean():.3f} mm/s')
        axes[0, 1].legend(fontsize=16, framealpha=0.9)
        axes[0, 1].grid(True, alpha=0.4, color=self.colors['primary'])
        
        # Speed vs Distance with enhanced gradient
        scatter = axes[1, 0].scatter(df['total_distance_mm'], df['average_speed_mm_s'], 
                                   alpha=0.8, c=df['activity_level'], 
                                   cmap='plasma', s=100, edgecolors=self.colors['primary'], linewidth=2)
        axes[1, 0].set_xlabel('Total Distance (mm)', fontsize=18, color=self.colors['text'])
        axes[1, 0].set_ylabel('Average Speed (mm/s)', fontsize=18, color=self.colors['text'])
        axes[1, 0].set_title('🎯 Speed vs Distance Relationship', fontsize=20, color=self.colors['info'])
        axes[1, 0].grid(True, alpha=0.4, color=self.colors['primary'])
        cbar = plt.colorbar(scatter, ax=axes[1, 0])
        cbar.set_label('Activity Level', fontsize=16, color=self.colors['text'])
        cbar.ax.tick_params(colors=self.colors['text'])
        
        # Speed vs Activity Level with trend line
        axes[1, 1].scatter(df['activity_level'], df['average_speed_mm_s'], alpha=0.8, 
                          color=self.colors['secondary'], s=100, edgecolors=self.colors['primary'], linewidth=2)
        axes[1, 1].set_xlabel('Activity Level', fontsize=18, color=self.colors['text'])
        axes[1, 1].set_ylabel('Average Speed (mm/s)', fontsize=18, color=self.colors['text'])
        axes[1, 1].set_title('💫 Speed vs Activity Level', fontsize=20, color=self.colors['success'])
        axes[1, 1].grid(True, alpha=0.4, color=self.colors['primary'])
        
        # Add trend line (with data validation)
        valid_data = df.dropna(subset=['activity_level', 'average_speed_mm_s'])
        if len(valid_data) > 1 and valid_data['activity_level'].std() > 0:
            try:
                z = np.polyfit(valid_data['activity_level'], valid_data['average_speed_mm_s'], 1)
                p = np.poly1d(z)
                axes[1, 1].plot(valid_data['activity_level'], p(valid_data['activity_level']), 
                               color=self.colors['warning'], linestyle='--', linewidth=4, alpha=0.9)
            except:
                pass  # Skip trend line if polyfit fails
        
        # Add correlation coefficient
        corr = df['activity_level'].corr(df['average_speed_mm_s'])
        axes[1, 1].text(0.05, 0.95, f'Correlation: {corr:.3f}', 
                       transform=axes[1, 1].transAxes, fontsize=16, 
                       bbox=dict(boxstyle="round,pad=0.5", facecolor=self.colors['dark'], 
                               edgecolor=self.colors['primary'], alpha=0.9, linewidth=2),
                       color=self.colors['text'])
        
        plt.tight_layout()
        plt.savefig(self.output_dir / 'radium_speed_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
    
    def create_all_enhanced_visualizations(self, metrics_file: str, summary_file: str):
        """Create all enhanced visualizations"""
        print("Loading data...")
        df, summary = self.load_data(metrics_file, summary_file)
        
        print("Creating enhanced dashboard...")
        self.create_enhanced_dashboard(df, summary)
        
        print("Creating radium speed analysis...")
        self.create_radium_speed_analysis(df)
        
        print(f"Enhanced visualizations saved to {self.output_dir}")

def main():
    parser = argparse.ArgumentParser(description='Enhanced Behavioral Analysis Visualization')
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
    
    print("Starting Enhanced Behavioral Analysis Visualization...")
    print(f"Metrics file: {args.metrics_file}")
    print(f"Summary file: {args.summary_file}")
    print(f"Output directory: {args.output_dir}")
    
    visualizer = EnhancedBehavioralVisualizer(args.output_dir)
    visualizer.create_all_enhanced_visualizations(args.metrics_file, args.summary_file)
    
    print("Enhanced visualization complete!")

if __name__ == "__main__":
    main()
