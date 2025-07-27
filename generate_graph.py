import requests
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from matplotlib.patches import Rectangle

USERNAME = "arnab9957"

def get_contributions(username):
    """Fetch GitHub contributions data for the user"""
    url = f"https://github-contributions-api.deno.dev/{username}.json"
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        data = res.json()
    except requests.RequestException as e:
        print(f"Error fetching contributions: {e}")
        return [], []
    
    today = datetime.date.today()
    dates, counts = [], []

    for week in data["contributions"]:
        for day in week["days"]:
            date = datetime.datetime.strptime(day["date"], "%Y-%m-%d").date()
            if (today - date).days <= 365:  # Show last year of data
                dates.append(date)
                counts.append(day["count"])

    return dates, counts

def plot_contributions(dates, counts):
    """Create a beautiful contribution graph"""
    if not dates or not counts:
        print("No contribution data available")
        return
    
    # Create figure with dark theme
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(16, 6))
    
    # Create gradient colors based on contribution count
    max_count = max(counts) if counts else 1
    colors = []
    for count in counts:
        if count == 0:
            colors.append('#161b22')  # Dark gray for no contributions
        elif count <= max_count * 0.25:
            colors.append('#0e4429')  # Dark green
        elif count <= max_count * 0.5:
            colors.append('#006d32')  # Medium green
        elif count <= max_count * 0.75:
            colors.append('#26a641')  # Light green
        else:
            colors.append('#39d353')  # Bright green
    
    # Plot the contribution graph
    bars = ax.bar(dates, counts, color=colors, width=1, edgecolor='black', linewidth=0.1)
    
    # Customize the plot
    ax.set_title(f"🔥 {USERNAME}'s Daily GitHub Contributions", 
                fontsize=20, fontweight='bold', color='#58a6ff', pad=20)
    ax.set_xlabel("Date", fontsize=14, color='white')
    ax.set_ylabel("Contributions", fontsize=14, color='white')
    
    # Format x-axis
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    ax.xaxis.set_minor_locator(mdates.WeekdayLocator())
    
    # Rotate x-axis labels
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    # Add grid
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    
    # Add statistics text
    total_contributions = sum(counts)
    avg_contributions = total_contributions / len(counts) if counts else 0
    max_contributions = max(counts) if counts else 0
    
    stats_text = f"📊 Total: {total_contributions} | 📈 Avg: {avg_contributions:.1f}/day | 🏆 Max: {max_contributions}/day"
    ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, 
            fontsize=12, verticalalignment='top', color='#f0f6fc',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#21262d', alpha=0.8))
    
    # Add current date
    current_date = datetime.datetime.now().strftime("%B %d, %Y")
    ax.text(0.98, 0.02, f"Last updated: {current_date}", transform=ax.transAxes,
            fontsize=10, horizontalalignment='right', color='#8b949e')
    
    # Tight layout and save
    plt.tight_layout()
    plt.savefig("contribution_graph.png", dpi=300, bbox_inches='tight', 
                facecolor='#0d1117', edgecolor='none')
    plt.close()
    
    print(f"✅ Contribution graph generated successfully!")
    print(f"📈 Total contributions in the last year: {total_contributions}")

if __name__ == "__main__":
    print("🚀 Generating GitHub contribution graph...")
    dates, counts = get_contributions(USERNAME)
    plot_contributions(dates, counts)
