import csv

def read_csv_file(file_path):
    data = []

    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)

        # Read the first row to determine the number of columns
        first_row = next(csv_reader)
        num_columns = len(first_row)

        # Initialize lists for each column
        columns = [[] for _ in range(num_columns)]

        # Convert the first row to floats and append to the respective columns
        for i, value in enumerate(first_row):
            try:
                columns[i].append(float(value))
            except ValueError:
                pass  # Ignore non-numeric values

        # Process the rest of the rows
        for row in csv_reader:
            for i, value in enumerate(row):
                try:
                    columns[i].append(float(value))
                except ValueError:
                    pass  # Ignore non-numeric values

    return columns

