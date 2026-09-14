import os
import requests
from dotenv import load_dotenv

# Cargar las variables del archivo .env
load_dotenv()

APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")

# Petición de prueba: buscar ofertas de "python" en España, página 1
url = f"https://api.adzuna.com/v1/api/jobs/es/search/1"
params = {
    "app_id": APP_ID,
    "app_key": APP_KEY,
    "results_per_page": 5,
    "what": "python"
}

response = requests.get(url, params=params)

print("Status code:", response.status_code)
print(response.json())