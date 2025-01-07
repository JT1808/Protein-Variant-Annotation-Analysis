import pandas as pd
import re
# Load the Excel file
file_path = '/Users/op/Documents/FinalVersion/pythonProject1/uniprot-protein.xlsx'  # Update with your file path
df = pd.read_excel(file_path)


# Extract relevant columns
df = df[['Entry', 'Domain [FT]']].dropna()

# Function to extract the Protein kinase range
def extract_protein_kinase_range(text):
    # Split the text into individual domain entries
    domains = text.split('DOMAIN ')
    for domain in domains:
        # Check if "Protein kinase" is in the domain annotation
        if "Protein kinase" in domain:
            # Extract the range (e.g., "242..493")
            match = re.search(r'(\d+\.\.\d+)', domain)
            if match:
                return match.group(1)  # Return the range
    return None  # Return None if no Protein kinase domain is found

# Apply the function to extract ranges
df['Protein Kinase Range'] = df['Domain [FT]'].apply(extract_protein_kinase_range)

# Drop rows without a Protein kinase range
df = df.dropna(subset=['Protein Kinase Range'])

# Keep only the required columns
df = df[['Entry', 'Protein Kinase Range']]

# Display the result
print(df)

# Optionally, save the result to a CSV file
df.to_csv('protein_kinase_ranges_final.csv', index=False)