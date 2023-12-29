import os
import json
import requests

ORG_NAME = "github-gk-aks"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# Fetch all repositories in the organization
url = f"https://api.github.com/orgs/{ORG_NAME}/repos?per_page=100"
response = requests.get(url, headers=headers)
repos = response.json()

if isinstance(repos, str):
    repos = json.loads(repos)

# Filter out archived repositories
active_repos = [repo["full_name"] for repo in repos if not repo["archived"]]

# Write the list of repositories to a text file
with open("repo_list.txt", "w") as f:
    for repo in active_repos:
        f.write(f"{repo}\n")
