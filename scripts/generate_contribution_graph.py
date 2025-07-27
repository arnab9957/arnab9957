import requests
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def fetch_github_contributions(username, token):
    """Fetch contribution data from GitHub API"""
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    # Get user's repositories
    repos_url = f'https://api.github.com/users/{username}/repos'
    repos_response = requests.get(repos_url, headers=headers)
    repos = repos_response.json()
    
    contributions = {}
    
    # Get commits from each repository
    for repo in repos:
        if repo['owner']['login'] == username:  # Only user's own repos
            commits_url = f"https://api.github.com/repos/{username}/{repo['name']}/commits"
            params = {
                'author': username,
                'since': (datetime.now() - timedelta(days=365)).isoformat(),
                'per_page': 100
            }
            
            try:
                commits_response = requests.get(commits_url, headers=headers, params=params)
                commits = commits_response.json()
                
                for commit in commits:
                    if isinstance(commit, dict) and 'commit' in commit:
                        date = commit['commit']['author']['date'][:10]  # YYYY-MM-DD
                        contributions[date] = contributions.get(date, 0) + 1
            except:
                continue
    
    return contributions

def create_contribution_graph(contributions, username):
    """Create a GitHub-style contribution graph"""
    # Set up the style
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(15, 4))
    
    # Create date range for the last year
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    # Create a complete date range
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Convert contributions to DataFrame
    contribution_data = []
    for date in date_range:
        date_str = date.strftime('%Y-%m-%d')
        count = contributions.get(date_str, 0)
        contribution_data.append({
            'date': date,
            'contributions': count,
            'week': date.isocalendar()[1],
            'weekday': date.weekday()
        })
    
    df = pd.DataFrame(contribution_data)
    
    # Create pivot table for heatmap
    pivot_table = df.pivot_table(
        values='contributions', 
        index='weekday', 
        columns='week', 
        fill_value=0
    )
    
    # Define color map (GitHub-style)
    colors = ['#0d1117', '#0e4429', '#006d32', '#26a641', '#39d353']
    n_colors = len(colors)
    
    # Normalize contribution counts to color indices
    max_contributions = df['contributions'].max()
    if max_contributions > 0:
        normalized_data = (pivot_table / max_contributions * (n_colors - 1)).round().astype(int)
    else:
        normalized_data = pivot_table * 0
    
    # Create custom colormap
    from matplotlib.colors import ListedColormap
    cmap = ListedColormap(colors)
    
    # Create heatmap
    sns.heatmap(
        normalized_data,
        cmap=cmap,
        cbar=False,
        square=True,
        linewidths=1,
        linecolor='#21262d',
        ax=ax,
        vmin=0,
        vmax=n_colors-1
    )
    
    # Customize the plot
    ax.set_title(f'{username}\'s Contribution Graph - Last 365 Days', 
                fontsize=16, color='white', pad=20)
    
    # Set y-axis labels (days of week)
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    ax.set_yticklabels(days, rotation=0, fontsize=10)
    
    # Remove x-axis labels for cleaner look
    ax.set_xticklabels([])
    ax.set_xlabel('')
    ax.set_ylabel('')
    
    # Add contribution summary
    total_contributions = df['contributions'].sum()
    active_days = (df['contributions'] > 0).sum()
    
    plt.figtext(0.02, 0.02, 
                f'Total: {total_contributions} contributions • Active days: {active_days}',
                fontsize=10, color='#7d8590')
    
    # Save the plot
    plt.tight_layout()
    plt.savefig('contribution_graph.png', 
                dpi=300, 
                bbox_inches='tight', 
                facecolor='#0d1117',
                edgecolor='none')
    plt.close()

def main():
    username = 'arnab9957'  # Your GitHub username
    token = os.environ.get('GITHUB_TOKEN')
    
    if not token:
        print("GitHub token not found!")
        return
    
    print("Fetching contribution data...")
    contributions = fetch_github_contributions(username, token)
    
    print("Generating contribution graph...")
    create_contribution_graph(contributions, username)
    
    print("Contribution graph updated successfully!")

if __name__ == "__main__":
    main()
