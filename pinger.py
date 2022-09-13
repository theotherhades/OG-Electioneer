import time, requests, server

while True:
    time.sleep(60)
    requests.get(f"{server.url}/ping")