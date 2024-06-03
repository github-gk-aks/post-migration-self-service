import os
import json
import requests
import sys

ORG_NAME = "github-gk-aks"
GITHUB_TOKEN = os.environ['GK_PAT']
repo_name = sys.argv[1]  # Repository name passed as a command line argument

def get_repo_size(owner, repo, token):
    url = f"https://api.github.com/repos/{ORG_NAME}/{repo}"

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        repo_info = response.json()
        size_kb = repo_info.get('size', 0)
        size_mb = size_kb / 1024
        return size_mb
    else:
        raise Exception(f"Failed to fetch repository info: {response.status_code}")

try:
    size_mb = get_repo_size(ORG_NAME, repo_name, GITHUB_TOKEN)
    print(f"The size of the repository is {size_mb:.2f} MB")
      
    # Create a file with repository name and size
    with open(f"report_{repo_name}.txt", "w") as file:
        file.write(f"Repository: {repo_name}\nSize: {size_mb:.2f} MB")

except Exception as e:
    print(e)
