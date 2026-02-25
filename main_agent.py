import time
from system_monitor import check_hardware
from healthcheck import run_healthcheck

list_url = ["https://google.com", "https://api.github.com", "https://httpbin.org/status/404", "https://httpbin.org/status/500","https://adres-ktory-na-pewno-nie-istnieje-12345.com"]

while True:
    print("=== URUCHAMIAM CYKL SPRAWDZAJĄCY ===")
    check_hardware()
    run_healthcheck(list_url)
    print("=== OCZEKIWANIE 10S ====")
    time.sleep(10)
