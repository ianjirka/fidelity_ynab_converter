import os
import glob
import pandas as pd

#Find the most recent file in the Downloads folder
user_profile_path = os.getenv('USERPROFILE')
downloads_path = user_profile_path + '/Downloads/'
search_str = "History_for_Account_*.csv" 
search_path = os.path.join(downloads_path, search_str)

files = glob.glob(search_path) 
files.sort(key=os.path.getmtime, reverse=True)

if not files: 
    print("No matching files found.")
    exit(1)

most_recent_file = files[0] 
print(f"Found most recent file: {most_recent_file}")

# Open the file
with open(most_recent_file, 'r') as file:
    # Read lines until 'Run Date' is found
    for i, line in enumerate(file):
        if 'Run Date' in line:
            break

# Read the CSV into a DataFrame, skipping rows before 'Run Date'
df = pd.read_csv(most_recent_file, skiprows=i)

# Reset the index
df = df.reset_index(drop=True)

#Remove any rows where 'Run Date' cannot be converted to a date
df = df[pd.to_datetime(df['Run Date'], errors='coerce').notna()]

#Create a YNAB compatible DataFrame
df_ynab = pd.DataFrame()
df_ynab['Date'] = pd.to_datetime(df['Run Date']).dt.strftime('%m/%d/%Y')
df_ynab['Amount'] = df['Amount ($)'] 
df_ynab['Description'] = df['Action']

# Write the DataFrame to a new CSV file
output_file = downloads_path + "YNAB_Import.csv"
df_ynab.to_csv(output_file, index=False)
print(f"Formatted CSV saved as {output_file}")
os.remove(most_recent_file)

# Delete all .qxf files in the Downloads directory
qxf_files = glob.glob(os.path.join(downloads_path, '*.qfx'))
if not qxf_files:
    print("No .qxf files found.")
else:
    for qxf_file in qxf_files:
        os.remove(qxf_file)
        print(f"Deleted file: {qxf_file}")