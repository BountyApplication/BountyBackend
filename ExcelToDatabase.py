import csv
import sys
import requests

def send_post_request(url, data):
    response = requests.post(url, json=data)
    return response

def main():
    if len(sys.argv) > 1:
        csv_file_path = sys.argv[1]
    else:
        csv_file_path = input("Pfad zur CSV-Datei: ")
    url = "http://127.0.0.1:9000/bounty/accounts"
    method = "POST"

    try:
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
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
    except UnicodeDecodeError:
        print("Fehler: Die Datei ist nicht UTF-8 kodiert. In Excel beim Export 'CSV UTF-8 (Trennzeichen-getrennt)' statt 'CSV (Trennzeichen-getrennt)' wählen.")

if __name__ == "__main__":
    main()