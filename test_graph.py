#!/usr/bin/env python3
"""
Test script to generate a sample contribution graph
Run this locally to test before setting up GitHub Actions
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from datetime import datetime, timedelta
import random

def create_sample_contribution_graph():
    """Create a sample contribution graph with mock data"""
    fig, ax = plt.subplots(figsize=(16, 4), facecolor='#0d1117')
    ax.set_facecolor('#0d1117')
    
    # GitHub color scheme
    colors = {
        0: '#161b22',    # No contributions
        1: '#0e4429',    # Low
        2: '#006d32',    # Medium-low  
        3: '#26a641',    # Medium-high
        4: '#39d353'     # High
    }
    
    # Generate 52 weeks of sample data
    weeks = 52
    days_per_week = 7
    
    # Create sample contribution data
    np.random.seed(42)  # For reproducible results
    contribution_data = []
    
    for week in range(weeks):
        week_data = []
        for day in range(days_per_week):
            # Simulate realistic contribution patterns
            # Higher chance of contributions on weekdays
            if day < 5:  # Weekdays
                contrib = np.random.choice([0, 1, 2, 3, 4], p=[0.3, 0.3, 0.2, 0.15, 0.05])
            else:  # Weekends
                contrib = np.random.choice([0, 1, 2, 3, 4], p=[0.6, 0.25, 0.1, 0.04, 0.01])
            week_data.append(contrib)
        contribution_data.append(week_data)
    
    # Draw the contribution squares
    square_size = 0.8
    gap = 0.2
    
    total_contributions = 0
    for week_idx, week in enumerate(contribution_data):
        for day_idx, level in enumerate(week):
            # Convert level to actual contribution count for display
            contrib_count = [0, 3, 7, 12, 20][level]
            total_contributions += contrib_count
            
            # Draw square
            rect = patches.Rectangle(
                (week_idx * (square_size + gap), day_idx * (square_size + gap)),
                square_size, square_size,
                facecolor=colors[level],
                edgecolor='#21262d',
                linewidth=0.5
            )
            ax.add_patch(rect)
    
    # Set up the plot
    ax.set_xlim(-0.5, weeks * (square_size + gap))
    ax.set_ylim(-0.5, days_per_week * (square_size + gap))
    
    # Add day labels
    days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    for i, day in enumerate(days):
        ax.text(-1, i * (square_size + gap) + square_size/2, day, 
                ha='right', va='center', color='#7d8590', fontsize=10)
    
    # Add month labels
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    for i, month in enumerate(months):
        if i * 4.33 < weeks:  # Approximate weeks per month
            ax.text(i * 4.33 * (square_size + gap) + square_size/2, -1, month,
                   ha='center', va='top', color='#7d8590', fontsize=10)
    
    # Title and stats
    ax.text(weeks * (square_size + gap) / 2, 8, 
            'arnab9957\'s Contribution Graph', 
            ha='center', va='bottom', color='white', fontsize=16, weight='bold')
    
    ax.text(weeks * (square_size + gap) / 2, -2.5,
            f'{total_contributions} contributions in the last year',
            ha='center', va='top', color='#7d8590', fontsize=12)
    
    # Add legend
    legend_x = weeks * (square_size + gap) - 15
    legend_y = -3
    ax.text(legend_x, legend_y, 'Less', ha='left', va='center', color='#7d8590', fontsize=9)
    
    for i, color in enumerate(colors.values()):
        rect = patches.Rectangle(
            (legend_x + 2 + i * 1.2, legend_y - 0.3),
            0.8, 0.8,
            facecolor=color,
            edgecolor='#21262d',
            linewidth=0.5
        )
        ax.add_patch(rect)
    
    ax.text(legend_x + 8, legend_y, 'More', ha='left', va='center', color='#7d8590', fontsize=9)
    
    # Remove axes
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    plt.tight_layout()
    plt.savefig('contribution_graph.png', 
                dpi=300, 
                bbox_inches='tight',
                facecolor='#0d1117',
                edgecolor='none')
    plt.close()
    
    print("Sample contribution graph created successfully!")
    print("File saved as: contribution_graph.png")

if __name__ == "__main__":
    create_sample_contribution_graph()
