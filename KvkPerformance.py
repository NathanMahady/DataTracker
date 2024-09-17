import pandas as pd

# Load both CSV files into pandas DataFrames
file1 = '2449Top300_12_09.csv'
file2 = '2449Top300_17_09.csv'

# Read the CSV files
df1 = pd.read_csv(file1, encoding='utf-8')
df2 = pd.read_csv(file2, encoding='utf-8')

df1.columns = df1.columns.str.strip()
df2.columns = df2.columns.str.strip()

# Drop rows where all values are NaN
df1.dropna(how='all', inplace=True)
df2.dropna(how='all', inplace=True)

# Merge the data on 'ID' to get players that are in both sheets, and use the second sheet's username
merged_df = pd.merge(df1, df2, on='ID', suffixes=('_1', '_2'))

# Create a new DataFrame to store the differences and relevant information
result_df = pd.DataFrame()

# Copy the username from the second sheet
result_df['Username'] = merged_df['Username_2']

# Copy the 'ID' column (since it's the same in both sheets)
result_df['ID'] = merged_df['ID']

for column in ['Power', 'KP', 'TotalDeads', 'T1', 'T2', 'T3', 'T4', 'T5']:
    # Convert string to numeric (handling commas), coerce errors to NaN
    merged_df[f'{column}_1'] = pd.to_numeric(merged_df[f'{column}_1'].replace({',': ''}, regex=True), errors='coerce')
    merged_df[f'{column}_2'] = pd.to_numeric(merged_df[f'{column}_2'].replace({',': ''}, regex=True), errors='coerce')
    
    # Calculate the difference and fill NaN values with zeroes
    result_df[column] = (merged_df[f'{column}_2'] - merged_df[f'{column}_1']).fillna(0)

# Export the resulting DataFrame to a new CSV file
output_file = 'players_difference.csv'
result_df.to_csv(output_file, index=False, encoding='utf-8')

print(f'Difference file created: {output_file}')
