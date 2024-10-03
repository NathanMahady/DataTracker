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

# Merge the data on 'ID' using outer join, ensuring all rows from both df1 and df2 are included
merged_df = pd.merge(df1, df2, on='ID', how='outer', suffixes=('_1', '_2'))

# Create a new DataFrame to store the differences and relevant information
result_df = pd.DataFrame()

# Use the Username from the second sheet if it exists, otherwise fallback to the first sheet's Username
result_df['Username'] = merged_df['Username_2'].combine_first(merged_df['Username_1'])

# Copy the 'ID' column (since it's the same in both sheets)
result_df['ID'] = merged_df['ID']

# Process the columns that require calculating differences for KP, Deads, T1-T5
for column in ['KP', 'TotalDeads', 'T1', 'T2', 'T3', 'T4', 'T5']:
    # Convert string to numeric (handling commas), coerce errors to NaN
    merged_df[f'{column}_1'] = pd.to_numeric(merged_df[f'{column}_1'].replace({',': ''}, regex=True), errors='coerce')
    merged_df[f'{column}_2'] = pd.to_numeric(merged_df[f'{column}_2'].replace({',': ''}, regex=True), errors='coerce')
    
    # Calculate the difference between df2 and df1, fill NaN with zeros
    result_df[column] = (merged_df[f'{column}_2'].fillna(0) - merged_df[f'{column}_1'].fillna(0))

# Add the new boolean column 'InBothScans' to indicate if the player exists in both DataFrames
result_df['InBothScans'] = merged_df[['Username_1', 'Username_2']].notnull().all(axis=1)

# Merge the original scan data to get the starting power and username
df_original = df_original[['ID', 'Power', 'Username']].copy()  # Keep relevant columns ('ID', 'Power', 'Username')
df_original.rename(columns={'Power': 'Starting Power'}, inplace=True)  # Rename 'Power' to 'Starting Power'

# Convert the starting power to numeric, handling commas and invalid data
df_original['Starting Power'] = pd.to_numeric(df_original['Starting Power'].replace({',': ''}, regex=True), errors='coerce')

# Merge the original scan data into the result DataFrame using a LEFT join to ensure all original scan players are included
result_df = pd.merge(df_original, result_df, on='ID', how='left')

# Merge the df2 power to calculate the Power Change
df2 = df2[['ID', 'Power']]  # Keep only relevant columns from df2
df2.rename(columns={'Power': 'Current Power'}, inplace=True)  # Rename for clarity

# Merge df2 current power into the result DataFrame
result_df = pd.merge(result_df, df2, on='ID', how='left')

# Calculate Power Change as the difference between df2's Power and the original scan's Starting Power
result_df['Power Change'] = result_df['Current Power'] - result_df['Starting Power']

# Drop the 'Current Power' column as it's no longer needed
result_df.drop(columns=['Current Power'], inplace=True)

# If a player's username is missing in result_df, use the username from the original scan
result_df['Username'] = result_df['Username_y'].combine_first(result_df['Username_x'])

# Drop the extra 'Username_x' and 'Username_y' columns after combining them
result_df.drop(columns=['Username_x', 'Username_y'], inplace=True)

# Fill any NaN values in the following columns with zeroes (before renaming)
fillna_columns = ['Starting Power', 'Power Change', 'KP', 'TotalDeads', 'T1', 'T2', 'T3', 'T4', 'T5']
result_df[fillna_columns] = result_df[fillna_columns].fillna(0)

# Rename 'TotalDeads' to 'Deads'
result_df.rename(columns={'TotalDeads': 'Deads'}, inplace=True)

# Reorder the columns to place 'Starting Power' as the third column
result_df = result_df[['Username', 'ID', 'Starting Power', 'Power Change', 'KP', 'Deads', 'T1', 'T2', 'T3', 'T4', 'T5', 'InBothScans']]

# Prevent negative values in the following columns
non_negative_columns = ['KP', 'Deads', 'T1', 'T2', 'T3', 'T4', 'T5']
result_df[non_negative_columns] = result_df[non_negative_columns].clip(lower=0)

# Explicitly convert the 'InBothScans' column to boolean to handle the 0 replacement
result_df['InBothScans'] = result_df['InBothScans'].astype(bool)

# Export the resulting DataFrame to a new CSV file
output_file = 'players_difference.csv'
result_df.to_csv(output_file, index=False, encoding='utf-8')

print(f'File created with starting power and changes: {output_file}')