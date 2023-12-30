import os
import json
import requests

ORG_NAME = "github-gk-aks"
github_token = os.environ['GK_PAT']

headers = {
    "Authorization": f"Bearer {github_token}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28"
}

all_repositories = []
# Fetch all repositories in the organization
for page in range(1, 4):
    url = f"https://api.github.com/orgs/{ORG_NAME}/repos?per_page=5&page={page}"
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

    all_repositories.extend(repos)

# Filter out archived repositories
active_repos = [repo["full_name"] for repo in all_repositories if isinstance(repo, dict) and not repo.get("archived")]

# Write the list of repositories to a text file
with open("repo_list.txt", "w") as file:
    file.write("\n".join(active_repos))

print(f"Total repositories: {len(active_repos)}")
