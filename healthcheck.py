import requests

def run_healthcheck(list_url):
    for url in list_url:
        try:
            response = requests.get(url, timeout=3)
            if response.status_code == 200:
                print(f"[ONLINE] {url}")
            else:
                print(f"[WARNING] {url} zwrócił kod: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"[CRITICAL] Nie można połączyć z {url}")
        except Exception as e:
            print(f"Błąd. Powód: {e}.")
