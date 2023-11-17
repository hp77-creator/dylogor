import json
import requests
import time


def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def send_json_to_server(json_data, server_url):
    headers = {'Content-Type': 'application/json'}
    response = requests.post(server_url, json=json_data, headers=headers)

    if response.status_code == 200:
        print(f"JSON data successfully sent to {server_url}")
    else:
        print(f"Failed to send JSON data. Status code: {response.status_code}")


if __name__ == "__main__":
    json_file_path = "test_entry.json"  # Replace with the path to your JSON file
    server_url = "http://localhost:3000"  # Replace with the URL of your local server
    interval_seconds = 2  # Set the interval in seconds

    while True:
        json_data = read_json_file(json_file_path)
        send_json_to_server(json_data, server_url)

        # Wait for the specified interval before sending the next request
        time.sleep(interval_seconds)
