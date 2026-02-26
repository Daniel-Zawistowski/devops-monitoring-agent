from datetime import datetime
import os
import time
from system_monitor import check_hardware
from healthcheck import run_healthcheck

URLS_TO_CHECK = os.environ.get("URLS_TO_CHECK", "https://google.com,https://api.github.com,https://httpbin.org/status/404,https://httpbin.org/status/500,https://adres-ktory-na-pewno-nie-istnieje-12345.com").split(",")
CHECK_INTERVAL = int(os.environ.get("CHECK_INTERVAL", "60"))

def run_agent():
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{start_time}] [INFO] System Monitor Agent started. Interval: {CHECK_INTERVAL}s")
    
    while True:
        check_hardware()
        run_healthcheck(URLS_TO_CHECK)
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    run_agent()