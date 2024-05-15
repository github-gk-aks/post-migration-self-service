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

# Save the result to a new excel file
configure_emu_team.to_excel('configure-EMU-team-updated.xlsx', index=False)