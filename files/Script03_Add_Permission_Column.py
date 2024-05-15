import pandas as pd

# Load the Excel file
df = pd.read_excel('output.xlsx')

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
df['Permission'] = df['Team in EMU'].apply(get_permission)

# Write the updated DataFrame back to Excel
df.to_excel('your_file.xlsx', index=False)