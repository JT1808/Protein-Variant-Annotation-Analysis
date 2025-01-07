import pandas as pd

# File paths
final_file_path = '/Users/op/Documents/FinalVersion/pythonProject1/Final file.xlsm'
uniprot_file_path = '/Users/op/Documents/FinalVersion/pythonProject1/Uniprot DrV Final copy.xlsx'
output_file_path = '/Users/op/Documents/FinalVersion/pythonProject1/Generated_Strictly_Validated_PDB_File.xlsx'

# Function to parse range strings
def parse_range(range_str):
    try:
        start, end = map(int, range_str.split('..'))
        return start, end
    except:
        return None, None


# Step 1: Load and Process the UniProt File
uniprot_file_df = pd.read_excel(uniprot_file_path)
current_entry = None
processed_data = []

# Iterate through the UniProt file
for _, row in uniprot_file_df.iterrows():
    if row['Line'] == 'AC':
        # Identify new Entry
        current_entry = row['ID'].strip(';')  # Remove trailing semicolon
    elif row['Line'] == 'DR' and current_entry:
        # Process DR rows under the current Entry
        pdb_id = row['PDB ID']
        range_1 = row['Range 1']
        score = row['Score']

        if pd.notna(pdb_id) and pd.notna(range_1) and pd.notna(score):
            processed_data.append({
                'Entry': current_entry,
                'PDB ID': pdb_id,
                'Range': range_1,
                'Score': score
            })

# Convert processed UniProt data to a DataFrame
processed_uniprot_df = pd.DataFrame(processed_data)

# Step 2: Load and Process the Final File
final_file_df = pd.read_excel(final_file_path, sheet_name='NEW file')  # Adjust sheet name if necessary
adjusted_global_output_data = []

# Process each entry in the Final File
for _, row in final_file_df.iterrows():
    entry = row['Entry']
    protein_range = row['Protein kinase range']
    start, end = parse_range(protein_range)

    if start is None or end is None:
        continue

    # Adjust the range with a tolerance of ±10
    adjusted_start = start - 10
    adjusted_end = end + 10

    # Filter processed UniProt data for the current entry
    matches = processed_uniprot_df[processed_uniprot_df['Entry'] == entry]

    # Find overlapping ranges in the UniProt data
    valid_matches = []
    for _, match in matches.iterrows():
        uniprot_range = match['Range']
        if isinstance(uniprot_range, str) and '=' in uniprot_range:
            for subrange in uniprot_range.split('=')[1].split(','):
                try:
                    # Clean and parse the range
                    range_start, range_end = map(int, subrange.strip('.').split('-'))
                    if adjusted_start <= range_end and adjusted_end >= range_start:
                        # Calculate overlap closeness
                        closeness = abs(start - range_start) + abs(end - range_end)
                        valid_matches.append({
                            'Entry': entry,
                            'Input Range': protein_range,
                            'Closest PDB ID': match['PDB ID'],
                            'PDB Range': f"({range_start}, {range_end})",
                            'Score': match['Score'],
                            'Closeness': closeness
                        })
                except Exception:
                    continue

    # Select the best match: prioritize closeness, then score
    if valid_matches:
        best_match = sorted(valid_matches, key=lambda x: (x['Closeness'], x['Score']))[0]
        adjusted_global_output_data.append({
            'Entry': best_match['Entry'],
            'Input Range': best_match['Input Range'],
            'Closest PDB ID': best_match['Closest PDB ID'],
            'PDB Range': best_match['PDB Range'],
            'Score': best_match['Score']
        })

# Step 3: Save Final Output
adjusted_global_output_df = pd.DataFrame(adjusted_global_output_data, columns=[
    'Entry', 'Input Range', 'Closest PDB ID', 'PDB Range', 'Score'
])
adjusted_global_output_df.to_excel(output_file_path, index=False)

print(f"Adjusted output saved to: {output_file_path}")

#