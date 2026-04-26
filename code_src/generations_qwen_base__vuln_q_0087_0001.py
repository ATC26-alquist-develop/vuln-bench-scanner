import requests
import time

def check_server_availability(server_url):
    try:
        response = requests.get(server_url, timeout=5)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return False

def monitor_server(server_url, interval=60):
    while True:
        if check_server_availability(server_url):
            print(f"Server is available at {server_url}")
        else:
            print(f"Server is not available at {server_url}")
        time.sleep(interval)

if __name__ == "__main__":
    server_url = "http://yourserver.com"  # Replace with your server URL
    monitor_server(server_url)