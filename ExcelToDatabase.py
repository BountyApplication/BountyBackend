import csv
import requests

def send_post_request(url, data):
    response = requests.post(url, headers=data)
    return response

def main():
    csv_file_path = "data.csv"  # Replace this with the path to your CSV file
    url = "http://bounty.local:9000/bounty/accounts"
    method = "POST"

    with open(csv_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            first_name = row["Firstname"]
            last_name = row["Lastname"]
            balance = row["Balance"]

            params = {
                "firstname": first_name,
                "lastname": last_name,
                "balance": balance
            }

            response = send_post_request(url, params)
            print(f"Row - Firstname: {first_name}, Lastname: {last_name}, Balance: {balance}")
            print(f"Response: {response.status_code}, {response.text}")

if __name__ == "__main__":
    main()