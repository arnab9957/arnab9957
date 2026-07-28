import os
import re
import urllib.request
import json
import base64

username = "arnab9957"
wakatime_key = os.getenv("WAKATIME_API_KEY")
token = os.getenv("GITHUB_TOKEN")

readme_path = os.path.join(os.path.dirname(__file__), "README.md")

def update_wakatime_stats():
    if not wakatime_key:
        print("No WAKATIME_API_KEY provided.")
        return

    try:
        auth_header = "Basic " + base64.b64encode(wakatime_key.encode()).decode()
        url = "https://wakatime.com/api/v1/users/current/stats/last_7_days"
        req = urllib.request.Request(
            url,
            headers={
                "Authorization": auth_header,
                "User-Agent": "GitHub-Readme-Updater"
            }
        )
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8")).get("data", {})
            total_time = data.get("human_readable_total", "0 hrs")
            languages = data.get("languages", [])[:5]

            waka_md = "\n<div align=\"center\">\n\n"
            waka_md += f"[![WakaTime](https://wakatime.com/badge/user/d8adf08a-af79-4b3f-8d60-bf4bf22a9064.svg)](https://wakatime.com/@d8adf08a-af79-4b3f-8d60-bf4bf22a9064)\n\n"
            waka_md += f"### 📊 Weekly Coding Breakdown (Total: **{total_time}**)\n\n"
            waka_md += "| Language | Time Spent | Progress |\n| :--- | :--- | :--- |\n"

            for lang in languages:
                name = lang.get("name", "")
                text = lang.get("text", "")
                pct = lang.get("percent", 0.0)
                filled = int(round(pct / 100 * 15))
                bar = "█" * filled + "░" * (15 - filled)
                waka_md += f"| **{name}** | {text} | `{bar}` {pct:.1f}% |\n"

            waka_md += f"\n*⏱️ Stats powered by [WakaTime Profile](https://wakatime.com/@d8adf08a-af79-4b3f-8d60-bf4bf22a9064) — updated live*\n\n</div>\n"

            with open(readme_path, "r", encoding="utf-8") as f:
                readme_text = f.read()

            pattern = r"(<!-- START_SECTION:wakatime -->).*?(<!-- END_SECTION:wakatime -->)"
            if re.search(pattern, readme_text, flags=re.DOTALL):
                updated_readme = re.sub(
                    pattern,
                    f"\\1{waka_md}\\2",
                    readme_text,
                    flags=re.DOTALL
                )
                with open(readme_path, "w", encoding="utf-8") as f:
                    f.write(updated_readme)
                print("Successfully updated README.md with WakaTime stats!")
    except Exception as e:
        print(f"Error updating WakaTime stats: {e}")

def update_top_repos():
    if not token:
        print("GITHUB_TOKEN environment variable not set. Skipping top repos update.")
        return

    query = """
    query ($username: String!) {
      user(login: $username) {
        contributionsCollection {
          commitContributionsByRepository(maxRepositories: 100) {
            contributions {
              totalCount
            }
            repository {
              name
              nameWithOwner
              isFork
              stargazerCount
              url
              description
            }
          }
        }
      }
    }
    """

    variables = {"username": username}
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "GitHub-Readme-Updater"
        },
        data=json.dumps({"query": query, "variables": variables}).encode("utf-8")
    )

    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            if "errors" in res_data:
                print("GraphQL Errors:", res_data["errors"])
                return
            
            user = res_data.get("data", {}).get("user", {})
            if not user:
                print("User data not found in response.")
                return
                
            repo_contribs = user.get("contributionsCollection", {}).get("commitContributionsByRepository", [])
            source_repos = []
            for item in repo_contribs:
                repo = item.get("repository", {})
                contrib = item.get("contributions", {})
                if repo.get("isFork"):
                    continue
                source_repos.append({
                    "name": repo.get("name"),
                    "nameWithOwner": repo.get("nameWithOwner"),
                    "url": repo.get("url"),
                    "stars": repo.get("stargazerCount", 0),
                    "commits": contrib.get("totalCount", 0),
                    "description": repo.get("description", "")
                })
                
            source_repos.sort(key=lambda x: x["commits"], reverse=True)
            top_repos = source_repos[:6]
            
            if not top_repos:
                markdown_content = "\n<div align=\"center\">\n\nNo active source repository contributions found in the current period.\n\n</div>\n"
            else:
                markdown_content = "\n<div align=\"center\">\n\n| Repository | Stars | Contributions |\n| :--- | :--- | :--- |\n"
                for r in top_repos:
                    star_badge = f"![Stars](https://img.shields.io/github/stars/{r['nameWithOwner']}?style=flat-square&color=yellow)"
                    commit_badge = f"![Commits](https://img.shields.io/badge/commits-{r['commits']}-orange?style=flat-square)"
                    markdown_content += f"| **[{r['name']}]({r['url']})** | {star_badge} | {commit_badge} |\n"
                markdown_content += "\n</div>\n"
                
            with open(readme_path, "r", encoding="utf-8") as f:
                readme_text = f.read()
                
            pattern = r"(<!-- START_SECTION:top-repos -->).*?(<!-- END_SECTION:top-repos -->)"
            updated_readme = re.sub(
                pattern, 
                f"\\1{markdown_content}\\2", 
                readme_text, 
                flags=re.DOTALL
            )
            
            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(updated_readme)
                
            print("Successfully updated README.md with top source repositories contributions!")
    except Exception as e:
        print(f"An error occurred updating top repos: {e}")

if __name__ == "__main__":
    update_wakatime_stats()
    update_top_repos()
