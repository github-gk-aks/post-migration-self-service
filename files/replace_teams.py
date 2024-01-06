import os
import json

repo_path = './target_repo'
codeowners_location = os.environ.get('CODEOWNERS_LOCATION')

teams_to_replace = json.loads(os.environ.get('TEAMS', '[]').replace("'", "\""))

# Read and replace teams in the CODEOWNERS file
codeowners_path = os.path.join(repo_path, codeowners_location)
with open(codeowners_path, 'r') as file:
    content = file.read()

for team in teams_to_replace:
    content = content.replace(team['search'], team['replace'])

with open(codeowners_path, 'w') as file:
    file.write(content)