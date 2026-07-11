import os
import re
import urllib.request
import json

# Setup token and username
token = os.getenv("GITHUB_TOKEN")
username = "arnab9957"

if not token:
    print("GITHUB_TOKEN environment variable not set. Exiting.")
    exit(0)

# GraphQL query to get user's repositories and contributions
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
            exit(1)
        
        user = res_data.get("data", {}).get("user", {})
        if not user:
            print("User data not found in response.")
            exit(1)
            
        repo_contribs = user.get("contributionsCollection", {}).get("commitContributionsByRepository", [])
        
        # Filter out forks and keep source repos
        source_repos = []
        for item in repo_contribs:
            repo = item.get("repository", {})
            contrib = item.get("contributions", {})
            
            # Skip if repo is a fork
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
            
        # Sort by commit contributions descending
        source_repos.sort(key=lambda x: x["commits"], reverse=True)
        
        # Format the markdown table (show top 6 source repositories)
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
            
        # Read current README.md
        readme_path = os.path.join(os.path.dirname(__file__), "README.md")
        with open(readme_path, "r", encoding="utf-8") as f:
            readme_text = f.read()
            
        # Replace content between markers
        pattern = r"(<!-- START_SECTION:top-repos -->).*?(<!-- END_SECTION:top-repos -->)"
        updated_readme = re.sub(
            pattern, 
            f"\\1{markdown_content}\\2", 
            readme_text, 
            flags=re.DOTALL
        )
        
        # Write back to README.md
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(updated_readme)
            
        print("Successfully updated README.md with top source repositories contributions!")

except Exception as e:
    print(f"An error occurred: {e}")
    exit(1)
