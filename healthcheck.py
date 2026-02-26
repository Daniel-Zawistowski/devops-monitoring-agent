import os
import requests
from datetime import datetime
from system_monitor import send_discord_alert

def run_healthcheck(urls: list):

    script_dir = os.path.dirname(os.path.abspath(__file__))
    log_dir = os.path.join(script_dir, "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "healthcheck.log")
    
    tag = datetime.now().strftime("%Y%m%d_%H%M%S")

    for url in urls:
        url = url.strip()
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"[ONLINE] {url}")
            else:
                msg = f"WARNING: {url} returned status code: {response.status_code}"
                with open(log_file, "a") as f:
                    f.write(f"[{tag}] {msg}\n")
                send_discord_alert(msg)
                
        except Exception as e:
            error_msg = f"CRITICAL: Failed to connect to {url}. Error: {e}"
            with open(log_file, "a") as f:
                f.write(f"[{tag}] {error_msg}\n")
            send_discord_alert(error_msg)

if __name__ == "__main__":
    test_urls = ["https://google.com", "https://github.com"]
    run_healthcheck(test_urls)
