import pandas as pd

# Load the excel files
team_mapping = pd.read_excel('teams-mapping-from-Digital-EMU.xlsx')
configure_emu_team = pd.read_excel('configure-EMU-team-access.xlsx')

# Create a dictionary from team_mapping for easy lookup
team_dict = dict(zip(team_mapping['Team Name Digital'], team_mapping['Team Name EMU']))

# Define a function to apply on each row of configure_emu_team
def fill_team_in_emu(row):
    team_in_digital = row['Team/User in Digital']
    return team_dict.get(team_in_digital, 'NA')

# Apply the function to fill 'Team in EMU'
configure_emu_team['Team in EMU'] = configure_emu_team.apply(fill_team_in_emu, axis=1)

# Drop the unnecessary column
configure_emu_team = configure_emu_team.drop(columns=['Team/User in EMU'])

# Split the 'Team in EMU' column into a list of values
configure_emu_team['Team in EMU'] = configure_emu_team['Team in EMU'].str.split('\n')

# Explode the list into separate rows
configure_emu_team = configure_emu_team.explode('Team in EMU')

# Remove rows where 'Team in EMU' is 'NA'
configure_emu_team = configure_emu_team[configure_emu_team['Team in EMU'] != 'NA']

# Define a function to determine the permission
def get_permission(val):
    if pd.isnull(val):
        return ''
    elif 'admin' in val:
        return 'admin'
    elif 'write' in val:
        return 'push'
    else:
        return ''

# Apply the function to Column D to create the new Permission column
configure_emu_team['Permission'] = configure_emu_team['Team in EMU'].apply(get_permission)

# Write the updated DataFrame back to Excel
configure_emu_team.to_excel('your_file.xlsx', index=False)