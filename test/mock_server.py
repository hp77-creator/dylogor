import json
import requests
import time
from datetime import datetime
import random

level_arr = ['info', 'error', 'warn', 'debug']
resource_id_arr = ['server-1234', 'server-5678', 'server-1', 'server-2']
trace_id_arr = ['abc-xyz-123', 'abc-xyz-456', 'abc-xyz-789', 'abc-xyz-12']

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def mock_data(json_data):
    current_data = json_data
    for key in json_data:
        print("{} -> {}".format(key, json_data[key]))
        if key=='level':
            random.shuffle(level_arr)
            current_data[key] = level_arr[0]
        if key == 'resourceId':
            random.shuffle(level_arr)
            current_data[key] = resource_id_arr[0]
        if key == 'timestamp':
            current_time = datetime.now()
            formatted_date_time = current_time.strftime("%Y-%m-%dT%H:%M:%SZ")
            current_data[key] = formatted_date_time
            print(formatted_date_time)
        if key == 'traceId':
            random.shuffle(trace_id_arr)
            current_data[key] = trace_id_arr[0]
    return current_data

def send_json_to_server(json_data, server_url):
    headers = {'Content-Type': 'application/json'}
    json_data = mock_data(json_data)
    response = requests.post(server_url, json=json_data, headers=headers)

    if response.status_code == 200:
        print(f"JSON data successfully sent to {server_url}")
    else:
        print(f"Failed to send JSON data. Status code: {response.status_code}")


if __name__ == "__main__":
    json_file_path = "test_entry.json"  # Replace with the path to your JSON file
    server_url = "http://localhost:3000/"  # Replace with the URL of your local server
    interval_seconds = 10  # Set the interval in seconds
    json_data = read_json_file(json_file_path)
    mock_data(json_data)
    while True:
        json_data = read_json_file(json_file_path)
        send_json_to_server(json_data, server_url)

        # Wait for the specified interval before sending the next request
        time.sleep(interval_seconds)
