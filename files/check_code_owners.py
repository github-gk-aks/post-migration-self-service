import os
import subprocess

def check_code_owners(repo_name):
   repo_path = f"temp_repos/{repo_name}"  # Assuming you have a temporary directory for cloning repos
   code_owners_locations = []
   # Check for CODEOWNERS file in different locations
   locations_to_check = [".github/CODEOWNERS", "data/CODEOWNERS", "CODEOWNERS"]
   for location in locations_to_check:
       code_owners_path = os.path.join(repo_path, location)
       if os.path.exists(code_owners_path):
           code_owners_locations.append(location)
   return code_owners_locations  # Return the locations of CODEOWNERS files

if __name__ == "__main__":
   repos_file = "repo_list.txt"
   results_file = "results.txt"
   if not os.path.exists("temp_repos"):
       os.makedirs("temp_repos")
   with open(repos_file, "r") as f:
       repo_names = f.read().splitlines()
   with open(results_file, "w") as results:
       for repo_name in repo_names:
           code_owners_locations = check_code_owners(repo_name)
           if code_owners_locations:
               results.write(f"{repo_name}, {', '.join(code_owners_locations)}\n")
           else:
               results.write(f"{repo_name}, Not found\n")