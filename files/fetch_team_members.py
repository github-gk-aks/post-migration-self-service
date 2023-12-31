import requests
import openpyxl
import os

# Read repository names from the input file
with open('repositories.txt', 'r') as file:
    repositories = [line.strip() for line in file]

# Initialize Excel workbook and worksheet
workbook = openpyxl.Workbook()
worksheet = workbook.active
worksheet.append(['Repository', 'Team/User', 'Permission'])

# GitHub API base URL
GITHUB_TOKEN = os.environ['GK_PAT']
api_base_url = 'https://api.github.com'

# Fetch teams, members, and permissions for each repository
for repository in repositories:
    # Fetch teams for the repository
    org_name = repository.split('/')[0]
    headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28"
    }
    teams_url = f'{api_base_url}/repos/{repository}/teams'
    teams_response = requests.get(teams_url, headers=headers)
    teams_data = teams_response.json()

    # Iterate through teams and fetch members and permissions
    for team in teams_data:
        team_name = team['slug']
        permission_url = f'{api_base_url}/orgs/{org_name}/teams/{team_name}/repos/{repository}'
        headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3.repository+json",
        "X-GitHub-Api-Version": "2022-11-28"
        }
        permission_response = requests.get(permission_url, headers=headers)
        
        # permission_data = permission_response.json()
        if permission_response.status_code == 200:
            try:
                permission_data = permission_response.json()
                permissions = permission_data.get('permissions', {})
                permission_strings = []
                # Iterate through permissions and append to Excel worksheet
                for permission, value in permissions.items():
                    permission_strings.append(f"{permission}: {value}")
                    # worksheet.append([repository, f'Team: {team_name}', f'{permission}: {value}'])
                permissions_string = ", ".join(permission_strings)
                worksheet.append([repository, f'Team: {team_name}', permissions_string])
            except requests.exceptions.JSONDecodeError as e:
                print(f"Error decoding JSON for {permission_url}: {e}")
                print(f"Response content: {permission_response.content}")
                continue

            if 'permissions' not in permission_data:
                print(f"Invalid response for {permission_url}. Skipping...")
                continue  
        else:
            print(f"Non-200 status code ({permission_response.status_code}) for {permission_url}")     

    # Fetch individual users and their permissions for the repository - Outside Collaborators
    collaborators_url = f'{api_base_url}/repos/{repository}/collaborators?affiliation=outside'
    headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28"
    }
    collaborators_response = requests.get(collaborators_url, headers=headers)
   
    if collaborators_response.status_code == 200:
        collaborators_data = collaborators_response.json()
        outside_collaborator_usernames = set()  # Set to store Outside Collaborator usernames

        for collaborator in collaborators_data:
            username = collaborator['login']
            permission_url = f'{api_base_url}/repos/{repository}/collaborators/{username}/permission'
            headers = {
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28"
            }
            permission_response = requests.get(permission_url, headers=headers)

            # permission_data = permission_response.json()
            if permission_response.status_code == 200:
                try:
                    permission_data = permission_response.json()
                    # Iterate through permissions and append to Excel worksheet
                    permission = permission_data.get('role_name')
                    worksheet.append([repository, f'User: {username}', f'Permission: {permission}', f'Outside_Collaborator: {"Yes"}'])
                    outside_collaborator_usernames.add(username)
                except requests.exceptions.JSONDecodeError as e:
                    print(f"Error decoding JSON for {permission_url}: {e}")
                    print(f"Response content: {permission_response.content}")
                    continue

                if 'permission' not in permission_data:
                    print(f"Invalid response for {permission_url}. Skipping...")
                    continue  
            else:
                print(f"Non-200 status code ({permission_response.status_code}) for {permission_url}")

    # Fetch individual users and their permissions for the repository - Direct Collaborators
    collaboratorsD_url = f'{api_base_url}/repos/{repository}/collaborators?affiliation=direct'
    headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28"
    }
    collaboratorsD_response = requests.get(collaboratorsD_url, headers=headers)
   
    if collaboratorsD_response.status_code == 200:
         collaboratorsD_data = collaboratorsD_response.json()

    for collaboratorD in collaboratorsD_data:
        username = collaboratorD['login']

        if username in outside_collaborator_usernames:
            print(f"Skipping Direct Collaborator {username} as it is already added as an Outside Collaborator.")
            continue

        permission_url = f'{api_base_url}/repos/{repository}/collaborators/{username}/permission'
        headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
        }
        permission_response = requests.get(permission_url, headers=headers)

        # permission_data = permission_response.json()
        if permission_response.status_code == 200:
            try:
                permission_data = permission_response.json()
                # Iterate through permissions and append to Excel worksheet
                permission = permission_data.get('role_name')
                worksheet.append([repository, f'User: {username}', f'Permission: {permission}'])
            except requests.exceptions.JSONDecodeError as e:
                print(f"Error decoding JSON for {permission_url}: {e}")
                print(f"Response content: {permission_response.content}")
                continue

            if 'permission' not in permission_data:
                print(f"Invalid response for {permission_url}. Skipping...")
                continue  
        else:
            print(f"Non-200 status code ({permission_response.status_code}) for {permission_url}")

# Save the Excel file
workbook.save('teams_members_permissions.xlsx')
