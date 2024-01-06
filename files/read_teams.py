import openpyxl
import json

teams = []

workbook = openpyxl.load_workbook('data/CodeOwners-Team-Replacement.xlsx')
sheet = workbook.active

for row in sheet.iter_rows(min_row=2, values_only=True):
    teams.append({'search': row[0], 'replace': row[1]})

# Convert teams to a JSON string
teams_json = json.dumps(teams)

workbook.close()

#print(f"::set-output name=teams::{teams_json}")
print(json.dumps(teams))
