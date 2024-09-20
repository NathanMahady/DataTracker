import pandas as pd

# Load both CSV files into pandas DataFrames
file1 = '2449Top300_12_09.csv'
file2 = '2449Top300_17_09.csv'
original_scan = '2449Top300_12_09.csv'

# Read the CSV files
df1 = pd.read_csv(file1, encoding='utf-8')
df2 = pd.read_csv(file2, encoding='utf-8')
df_original = pd.read_csv(original_scan, encoding='utf-8')

# Strip any leading/trailing whitespaces from the column names
df1.columns = df1.columns.str.strip()
df2.columns = df2.columns.str.strip()
df_original.columns = df_original.columns.str.strip()

# Drop rows where all values are NaN
df1.dropna(how='all', inplace=True)
df2.dropna(how='all', inplace=True)
df_original.dropna(how='all', inplace=True)

# Merge the data on 'ID' to get players that are in both sheets, and use the second sheet's username
merged_df = pd.merge(df1, df2, on='ID', suffixes=('_1', '_2'))

# Create a new DataFrame to store the differences and relevant information
result_df = pd.DataFrame()

# Copy the username from the second sheet
result_df['Username'] = merged_df['Username_2']

# Copy the 'ID' column (since it's the same in both sheets)
result_df['ID'] = merged_df['ID']

# Process the columns that require calculating differences
for column in ['Power', 'KP', 'TotalDeads', 'T1', 'T2', 'T3', 'T4', 'T5']:
    # Convert string to numeric (handling commas), coerce errors to NaN
    merged_df[f'{column}_1'] = pd.to_numeric(merged_df[f'{column}_1'].replace({',': ''}, regex=True), errors='coerce')
    merged_df[f'{column}_2'] = pd.to_numeric(merged_df[f'{column}_2'].replace({',': ''}, regex=True), errors='coerce')
    
    # Calculate the difference and fill NaN values with zeroes
    result_df[column] = (merged_df[f'{column}_2'] - merged_df[f'{column}_1']).fillna(0)

# Merge the original scan data to get the starting power
df_original = df_original[['ID', 'Power']].copy()  # Keep only relevant columns ('ID' and 'Power')
df_original.rename(columns={'Power': 'Starting Power'}, inplace=True)  # Rename 'Power' to 'Starting Power'

# Convert the starting power to numeric, handling commas and invalid data
df_original['Starting Power'] = pd.to_numeric(df_original['Starting Power'].replace({',': ''}, regex=True), errors='coerce')

# Merge the starting power into the result DataFrame
result_df = pd.merge(result_df, df_original, on='ID', how='left')

# Fill any NaN values in the 'Starting Power' column with zeroes
result_df['Starting Power'] = result_df['Starting Power'].fillna(0)

# Rename 'Power' to 'Power Change' and 'TotalDeads' to 'Deads'
result_df.rename(columns={'Power': 'Power Change', 'TotalDeads': 'Deads'}, inplace=True)

# Reorder the columns to place 'Starting Power' as the third column
result_df = result_df[['Username', 'ID', 'Starting Power', 'Power Change', 'KP', 'Deads', 'T1', 'T2', 'T3', 'T4', 'T5']]

# Export the resulting DataFrame to a new CSV file
output_file = 'players_difference.csv'
result_df.to_csv(output_file, index=False, encoding='utf-8')

print(f'file created with starting power: {output_file}')
