import pandas as pd

# Load the two Excel files
df_source = pd.read_excel('Branches_and_Commit_Source.xlsx')
df_target = pd.read_excel('Branches_and_Commit_Target.xlsx')

# Merge the two dataframes, indicator=True will add a column '_merge' that indicates the source of each row
df = pd.merge(df_source, df_target, on=['Repository', 'Branch', 'Commit SHA'], how='outer', indicator=True)

# Create 'colour-code' and 'Remark' columns based on the conditions
df['colour-code'] = 'white'
df['Remark'] = 'Good'

df.loc[df['_merge'] == 'left_only', 'colour-code'] = 'RED'
df.loc[df['_merge'] == 'left_only', 'Remark'] = 'FAILED'

df.loc[(df['_merge'] == 'right_only') & df['Branch'].str.startswith('dependabot/'), 'colour-code'] = 'GREEN'
df.loc[(df['_merge'] == 'right_only') & df['Branch'].str.startswith('dependabot/'), 'Remark'] = 'SUCCESSFUL'

df.loc[(df['_merge'] == 'right_only') & ~df['Branch'].str.startswith('dependabot/'), 'colour-code'] = 'YELLOW'
df.loc[(df['_merge'] == 'right_only') & ~df['Branch'].str.startswith('dependabot/'), 'Remark'] = 'MANUAL REVIEW'

# Drop the '_merge' column
df = df.drop(columns='_merge')

# Write the result to a new Excel file
df.to_excel('final_report.xlsx', index=False)
