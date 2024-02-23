import pandas as pd
from openpyxl import load_workbook

# Read Excel_Input file
input_df = pd.read_excel('ACCESS_TOKEN_Input_File.xlsx')

# Load Excel_Output file with openpyxl to evaluate formulas
output_workbook = load_workbook('Digital_To_EMU_Input_Sheet.xlsx', data_only=True)
output_sheet = output_workbook.active
output_df = pd.DataFrame(output_sheet.values, columns=[cell.value for cell in output_sheet[1]])

# Merge the two dataframes on the 'Source Repo Name' column
merged_df = pd.merge(input_df, output_df[['Source Repo Name', 'Target Repo Name']], left_on='Repository', right_on='Source Repo Name', how='left')

# Replace the 'Repository' column with the 'Target Repo Name'
merged_df['Repository'] = merged_df['Target Repo Name']

# Drop the 'Target Repo Name' column
merged_df.drop('Target Repo Name', axis=1, inplace=True)

merged_df.drop('Source Repo Name',axis=1, inplace=True)

# Write the updated dataframe to a new Excel file
merged_df.to_excel('Transformed_Excel_Updated.xlsx', index=False)
