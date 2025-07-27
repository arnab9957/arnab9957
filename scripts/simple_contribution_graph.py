import requests
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from datetime import datetime, timedelta
import calendar
import os

def fetch_contribution_data(username):
    """Fetch contribution data using GitHub's GraphQL API"""
    token = os.environ.get('GITHUB_TOKEN')
    
    query = """
    query($username: String!) {
        user(login: $username) {
            contributionsCollection {
                contributionCalendar {
                    totalContributions
                    weeks {
                        contributionDays {
                            contributionCount
                            date
                        }
                    }
                }
            }
        }
    }
    """
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    response = requests.post(
        'https://api.github.com/graphql',
        json={'query': query, 'variables': {'username': username}},
        headers=headers
    )
    
    if response.status_code == 200:
        data = response.json()
        return data['data']['user']['contributionsCollection']['contributionCalendar']
    else:
        print(f"Error fetching data: {response.status_code}")
        return None

def create_github_style_graph(calendar_data, username):
    """Create a GitHub-style contribution graph"""
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
    
    weeks = calendar_data['weeks']
    total_contributions = calendar_data['totalContributions']
    
    # Find max contributions for scaling
    max_contributions = 0
    for week in weeks:
        for day in week['contributionDays']:
            max_contributions = max(max_contributions, day['contributionCount'])
    
    # Draw the contribution squares
    square_size = 0.8
    gap = 0.2
    
    for week_idx, week in enumerate(weeks):
        for day_idx, day in enumerate(week['contributionDays']):
            count = day['contributionCount']
            
            # Determine color level (0-4)
            if count == 0:
                level = 0
            elif count <= max_contributions * 0.25:
                level = 1
            elif count <= max_contributions * 0.5:
                level = 2
            elif count <= max_contributions * 0.75:
                level = 3
            else:
                level = 4
            
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
    ax.set_xlim(-0.5, len(weeks) * (square_size + gap))
    ax.set_ylim(-0.5, 7 * (square_size + gap))
    
    # Add day labels
    days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    for i, day in enumerate(days):
        ax.text(-1, i * (square_size + gap) + square_size/2, day, 
                ha='right', va='center', color='#7d8590', fontsize=10)
    
    # Add month labels
    current_month = None
    for week_idx, week in enumerate(weeks):
        if week['contributionDays']:
            date = datetime.strptime(week['contributionDays'][0]['date'], '%Y-%m-%d')
            month = date.strftime('%b')
            if month != current_month:
                ax.text(week_idx * (square_size + gap) + square_size/2, -1, month,
                       ha='center', va='top', color='#7d8590', fontsize=10)
                current_month = month
    
    # Title and stats
    ax.text(len(weeks) * (square_size + gap) / 2, 8, 
            f'{username}\'s Contribution Graph', 
            ha='center', va='bottom', color='white', fontsize=16, weight='bold')
    
    ax.text(len(weeks) * (square_size + gap) / 2, -2.5,
            f'{total_contributions} contributions in the last year',
            ha='center', va='top', color='#7d8590', fontsize=12)
    
    # Remove axes
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
    plt.tight_layout()
    plt.savefig('contribution_graph.png', 
                dpi=300, 
                bbox_inches='tight',
                facecolor='#0d1117',
                edgecolor='none')
    plt.close()

def main():
    username = 'arnab9957'
    
    print("Fetching contribution data from GitHub...")
    calendar_data = fetch_contribution_data(username)
    
    if calendar_data:
        print("Creating contribution graph...")
        create_github_style_graph(calendar_data, username)
        print("Contribution graph created successfully!")
    else:
        print("Failed to fetch contribution data")

if __name__ == "__main__":
    main()
