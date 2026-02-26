import psutil
import shutil
import os
from datetime import datetime
import requests

RAM_LIMIT = float(os.environ.get("RAM_LIMIT", "80.0"))
CPU_LIMIT = float(os.environ.get("CPU_LIMIT", "80.0"))
DISK_LIMIT = float(os.environ.get("DISK_LIMIT", "80.0"))
WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "")

def send_discord_alert(alert_message: str):
    if not WEBHOOK_URL:
        print(f"[WARNING] Webhook URL not configured. Cannot send alert: {alert_message}")
        return
    payload = {
            "username": "DevOps-Agent",
            "content": alert_message
    }
    try:
        requests.post(WEBHOOK_URL, json=payload, timeout=3)

    except Exception as e:
        print(f"Failed to send webhook: {e}")

def evaluate_metric(metric_name: str, current_value: float, limit: float, tag: str, alert_file: str):
    if current_value > limit:
        with open(alert_file, "a") as f:
            f.write(f"[{tag}] CRITICAL: {metric_name} usage exceeded {limit}% (Current: {round(current_value, 2)}%)\n")
        
        alert_message = f"CRITICAL: {metric_name} usage exceeded {limit}% (Current: {round(current_value, 2)}%)"
        send_discord_alert(alert_message)

def check_hardware():
    try:
        total, used, free = shutil.disk_usage("/")
        disk_usage = (used / total) * 100

        ram = psutil.virtual_memory()
        ram_usage = ram.percent

        cpu_usage = psutil.cpu_percent(interval=1)

        script_dir = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.join(script_dir, "logs")
        os.makedirs(base_path, exist_ok=True)

        alert_file = os.path.join(base_path, "alerts.log")
        tag = datetime.now().strftime("%Y%m%d_%H%M%S")
    
        evaluate_metric("RAM", ram_usage, RAM_LIMIT, tag, alert_file)
        evaluate_metric("CPU", cpu_usage, CPU_LIMIT, tag, alert_file)
        evaluate_metric("DISK", disk_usage, DISK_LIMIT, tag, alert_file)

    except Exception as e:
        print(f"Failed: {e}.")

if __name__ == "__main__":
    check_hardware()