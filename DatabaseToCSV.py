import json
import csv
import requests

def fetch_json(url):
    # Perform a GET request to fetch the JSON data
    response = requests.get(url)
    response.raise_for_status()  # Check for request errors
    return response.json()

def json_to_csv(json_data, csv_file_path):
    # Extract the keys (columns) from the first JSON object
    keys = json_data[0].keys()

    # Open the CSV file for writing
    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)

        # Write the header (column names)
        writer.writeheader()

        # Write the rows
        for item in json_data:
            writer.writerow(item)

# URL of the API endpoint returning JSON data
url = 'http://bounty.local:9000/bounty/accounts'

# Fetch the JSON data from the API
json_data = fetch_json(url)

# Path to the output CSV file
csv_file_path = 'output.csv'

# Convert JSON to CSV
json_to_csv(json_data, csv_file_path)

print(f"JSON data has been converted to CSV and saved to {csv_file_path}")
