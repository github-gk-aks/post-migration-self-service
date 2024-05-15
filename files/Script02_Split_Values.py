import pandas as pd

# Load your Excel file
df = pd.read_excel('configure-EMU-team-updated.xlsx')

# Split the 'Team in EMU' column into a list of values
df['Team in EMU'] = df['Team in EMU'].str.split('\n')

# Explode the list into separate rows
df = df.explode('Team in EMU')

# Remove rows where 'Team in EMU' is 'NA'
df = df[df['Team in EMU'] != 'NA']

# Save the result back to Excel
df.to_excel('output.xlsx', index=False)