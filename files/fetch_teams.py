import os
import requests
import openpyxl
from openpyxl import Workbook
from github import Github

GITHUB_TOKEN = os.environ['GK_PAT']
ORG_NAME = 'github-gk-aks'

def fetch_teams():
    url = f'https://api.github.com/orgs/{ORG_NAME}/teams?per_page=5'

    headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28"
    }
    
    # headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    response = requests.get(url, headers=headers)
    teams = response.json()
    return teams

def fetch_team_members(team_id):
    url = f'https://api.github.com/teams/{team_id}/members'

    headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28"
    }

    # headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    response = requests.get(url, headers=headers)
    members = response.json()
    return members

def main():
    teams = fetch_teams()

    # Create an Excel workbook
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = 'Teams'

    # Add headers
    sheet['A1'] = 'Team Name'
    sheet['B1'] = 'Members'

    # Add data
    row = 2
    for team in teams:
        team_name = team['name']
        team_id = team['id']
        members = fetch_team_members(team_id)
        member_names = ', '.join([member['login'] for member in members])

        sheet[f'A{row}'] = team_name
        sheet[f'B{row}'] = member_names

        row += 1

    # Save the workbook
    workbook.save('teams_and_members.xlsx')

if __name__ == '__main__':
    main()
