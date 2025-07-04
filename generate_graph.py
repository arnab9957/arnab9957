import requests
import datetime
import matplotlib.pyplot as plt

USERNAME = "arnab9957"

def get_contributions(username):
    url = f"https://github-contributions-api.deno.dev/{username}.json"
    res = requests.get(url)
    data = res.json()
    today = datetime.date.today()
    dates, counts = [], []

    for week in data["contributions"]:
        for day in week["days"]:
            date = datetime.datetime.strptime(day["date"], "%Y-%m-%d").date()
            if (today - date).days < 30:
                dates.append(date)
                counts.append(day["count"])

    return dates, counts

def plot_contributions(dates, counts):
    plt.figure(figsize=(10, 4))
    plt.plot(dates, counts, marker='o', color='lime')
    plt.title("My GitHub Contributions (Last 30 Days)")
    plt.xlabel("Date")
    plt.ylabel("Contributions")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("contribution_graph.png")
    plt.close()

if __name__ == "__main__":
    dates, counts = get_contributions(USERNAME)
    plot_contributions(dates, counts)
