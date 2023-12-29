import os
import json
import requests

ORG_NAME = "github-gk-aks"
github_token = os.environ['GK_PAT']

headers = {
    "Authorization": f"Bearer {github_token}",
    "Accept": "application/vnd.github.v3+json"
}

# Fetch all repositories in the organization
url = f"https://api.github.com/orgs/{ORG_NAME}/repos?per_page=100"
response = requests.get(url, headers=headers)

try:
    repos = response.json()
except json.JSONDecodeError:
    try:
        repos = json.loads(response.text)
    except json.JSONDecodeError:
        print("Error decoding JSON. Exiting.")
        print("Response content:")
        print(response.content.decode())
        exit(1)

# Check if the repos variable is a list (as expected)
if not isinstance(repos, list):
    print("Invalid JSON format. Exiting.")
    print("Response content:")
    print(response.content.decode())
    exit(1)

# Filter out archived repositories
active_repos = [repo["full_name"] for repo in repos if isinstance(repo, dict) and not repo.get("archived")]

# Write the list of repositories to a text file
with open("repo_list.txt", "w") as file:
    file.write("\n".join(active_repos))
