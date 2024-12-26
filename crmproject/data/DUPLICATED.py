import pandas as pd

# Load the CSV file
csv_file_path = 'raw_data.csv'
df = pd.read_csv(csv_file_path)

# Remove duplicates based on 'First Name' and 'Last Name' columns, keeping the first occurrence
df_cleaned = df.drop_duplicates(subset=['First Name', 'Last Name'], keep='first')

# Save the cleaned DataFrame back to a new CSV file
df_cleaned.to_csv('cleaned_file.csv', index=False)

print("Duplicate rows removed and saved to 'cleaned_file.csv'")
