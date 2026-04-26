import requests
import time
import logging

# Configure logging
logging.basicConfig(filename='server_monitor.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def check_server(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            logging.info(f'Server {url} is up and running.')
        else:
            logging.warning(f'Server {url} returned status code {response.status_code}.')
    except requests.exceptions.RequestException as e:
        logging.error(f'Error checking server {url}: {e}')

def main():
    server_url = 'http://example.com'  # Replace with the server URL you want to monitor
    check_interval = 60  # Check every 60 seconds

    while True:
        check_server(server_url)
        time.sleep(check_interval)

if __name__ == '__main__':
    main()