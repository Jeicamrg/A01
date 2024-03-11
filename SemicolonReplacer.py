import os

def replace_semicolon_with_comma_in_csv_files():
    """
    Opens all CSV files in the current directory,
    replaces all ';' signs with ',', and saves the modified content back to the same files.
    """

    # Get the current directory
    current_directory = os.getcwd()

    # List all files in the directory
    files = os.listdir(current_directory)

    # Filter out only the CSV files
    csv_files = [file for file in files if file.endswith('.csv')]

    # Iterate through each CSV file
    for csv_file in csv_files:
        file_path = os.path.join(current_directory, csv_file)
        
        # Open the file for reading and writing
        with open(file_path, 'r') as f:
            file_content = f.read()

        # Replace ';' with ','
        modified_content = file_content.replace(';', ',')

        # Write the modified content back to the file
        with open(file_path, 'w') as f:
            f.write(modified_content)

# Example usage:
replace_semicolon_with_comma_in_csv_files()
