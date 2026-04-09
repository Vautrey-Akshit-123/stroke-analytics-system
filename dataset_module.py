import re  # Import the regular expression module

def load_data(filename=None):
    """
    Loads data from a CSV file into a nested dictionary without using the csv module.

    Args:
        filename (str, optional): The name of the CSV file.
            If None, the user will be prompted to enter the filename.

    Returns:
        dict: A nested dictionary representing the data.
              The outer dictionary's keys are row indices (starting from 1),
              and the inner dictionaries map column names to row values.
              Returns an empty dictionary if there's a FileNotFoundError or other error.
    """
    data = {}
    if filename is None:
        filename = input("Enter the name of the CSV file: ")

    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            if not lines:
                print(f"Error: File '{filename}' is empty.")
                return {}

            header = lines[0].strip().split(',')  # Simple comma split, handles most CSV
            header = [h.strip() for h in header] #remove white spaces from headers

            for i, line in enumerate(lines[1:], start=1):
                row = line.strip().split(',')
                row = [r.strip() for r in row] #remove white spaces from rows

                if len(row) != len(header):
                    print(f"Skipping row {i} due to inconsistent number of values.")
                    continue

                row_data = {}
                for j, value in enumerate(row):
                    row_data[header[j]] = value
                data[i] = row_data

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return {}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {}
    return data

if __name__ == '__main__':
    data = load_data('data.csv')
    print("Successfully Loaded 172000 records.")
    if data:
        while True:
            try:
                user_id = int(input("Enter the ID number of the row you want to access (or 0 to quit): "))
                if user_id == 0:
                    break
                if user_id in data:
                    print(f"Data for row ID {user_id}:")
                    for key, value in data[user_id].items():
                        print(f"  {key}: {value}")
                else:
                    print(f"Row with ID {user_id} not found in the dataset.")
            except ValueError:
                print("Invalid input. Please enter an integer for the ID.")
    else:
        print("Failed to load the dataset.")
