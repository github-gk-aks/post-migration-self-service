import os
import subprocess
import requests

def get_default_branch(repo_name):
    # Make a GitHub API request to get information about the repository
    url = f"https://api.github.com/repos/{repo_name}"
    response = requests.get(url, headers={"Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}"})
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        repo_info = response.json()      
        # Extract and return the default branch
        default_branch = repo_info.get("default_branch")
        if default_branch is not None:
            return default_branch
        else:
            print("No value found for 'default_branch'.")
            return None
    else:
        # Handle the error if the request was not successful
        print(f"Error getting repository info for {repo_name}. Status code: {response.status_code}")
        return None  # Default to "master" in case of an error

def check_code_owners(repo_name):
    repo_path = f"temp_repos/{repo_name}"  # Assuming you have a temporary directory for cloning repos
    code_owners_locations = []
    # Check for CODEOWNERS file in different locations
    locations_to_check = [".github/CODEOWNERS", "docs/CODEOWNERS", "CODEOWNERS"]
    for location in locations_to_check:
        code_owners_path = os.path.join(repo_path, location)
        if os.path.exists(code_owners_path):
            code_owners_locations.append(location)
    return code_owners_locations  # Return the locations of CODEOWNERS files

if __name__ == "__main__":
    repos_file = "files/repo_list.txt"
    results_file = "results.txt"
    if not os.path.exists("temp_repos"):
        os.makedirs("temp_repos")

    with open(repos_file, "r") as f:
        repo_names = f.read().splitlines()

    with open(results_file, "w") as results:
        for repo_name in repo_names:
            # Clone the repository using GITHUB_TOKEN
            default_branch = get_default_branch(repo_name)
            if default_branch is not None:
                os.system(f"git clone https://github.com/{repo_name}.git temp_repos/{repo_name} --depth=1")
                code_owners_locations = check_code_owners(repo_name)
            
                if code_owners_locations:
                    results.write(f"{repo_name}, {', '.join(code_owners_locations)}\n")
                else:
                    results.write(f"{repo_name}, Not found\n")
            else:
                print(f"Skipping repository {repo_name} due to missing 'default_branch'.")
