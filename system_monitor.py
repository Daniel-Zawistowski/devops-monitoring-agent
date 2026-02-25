import psutil
import shutil
import os
from datetime import datetime
import requests

RAM_LIMIT = float(os.environ.get("RAM_LIMIT", "80.0"))
CPU_LIMIT = float(os.environ.get("CPU_LIMIT", "80.0"))
DISK_LIMIT = float(os.environ.get("DISK_LIMIT", "80.0"))
WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "")


def check_hardware():
    try:
# Analizujemy główny system plików Linuxa, czyli root ("/")
        total, used, free = shutil.disk_usage("/")
        procent_dysku = (used / total) * 100

        ram = psutil.virtual_memory()
        procent_ram = ram.percent

# Mierzymy CPU. Musimy podać czas (interval) w sekundach, 
# przez jaki badamy obciążenie, aby wynik był miarodajny.
        procent_cpu = psutil.cpu_percent(interval=1)

        base_path = "/home/daniel/road_to_devops/monitoring"
        print("Sprawdzam system...")
        os.makedirs(base_path, exist_ok=True)

        print(f"[SYSTEM STATUS] CPU: {round(procent_cpu, 2)} | RAM: {round(procent_ram, 2)} | DYSK: {round(procent_dysku, 2)}")

        alert_file = f"{base_path}/alerts.log"
        znacznik = datetime.now().strftime("%Y%m%d_%H%M%S")
    
        if procent_ram > RAM_LIMIT:
            with open(alert_file, "a") as f:
                f.write(f"[{znacznik}] CRITICAL: RAM przekroczył: {RAM_LIMIT} % (aktualnie: {round(procent_ram, 2)}%)\n")
            paczka_danych = {
            "username": "DevOps-Agent",
            "content": f"CRITICAL: RAM przekroczył: {RAM_LIMIT}% (aktualnie: {round(procent_ram, 2)}%)"
            }
            try:
                # Wysyłamy paczkę i prosimy Pythona, żeby nie czekał dłużej niż 3 sekundy
                requests.post(WEBHOOK_URL, json=paczka_danych, timeout=3)
                print(">>> Wysłano alert na Webhooka! <<<")
            except Exception as e:
                print(f"Nie udało się wysłać Webhooka. Błąd: {e}")
        if procent_cpu > CPU_LIMIT:
            with open(alert_file, "a") as f:
                f.write(f"[{znacznik}] CRITICAL: CPU przekroczył: {CPU_LIMIT} % (aktualnie: {round(procent_cpu, 2)}%)\n")
        if procent_dysku > DISK_LIMIT:
            with open(alert_file, "a") as f:
                f.write(f"[{znacznik}] CRITICAL: DYSK przekroczył: {DISK_LIMIT} % (aktualnie: {round(procent_dysku, 2)}%)\n")        

    except Exception as e:
        print(f"Błąd. Powód: {e}.")