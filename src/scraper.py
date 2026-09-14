import os
import time
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")

BASE_URL = "https://api.adzuna.com/v1/api/jobs/es/search/{page}"

# Skills/tecnologías sobre las que queremos datos
KEYWORDS = ["python", "java", "sql", "docker", "aws", "react", "machine learning"]

PAGINAS_POR_KEYWORD = 3  # cada página trae hasta 50 resultados (ajustable)
RESULTADOS_POR_PAGINA = 50


def buscar_ofertas(keyword, pagina):
    url = BASE_URL.format(page=pagina)
    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "results_per_page": RESULTADOS_POR_PAGINA,
        "what": keyword,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def recopilar_datos():
    todas_las_ofertas = []

    for keyword in KEYWORDS:
        print(f"Buscando ofertas para: {keyword}")
        for pagina in range(1, PAGINAS_POR_KEYWORD + 1):
            try:
                data = buscar_ofertas(keyword, pagina)
            except requests.exceptions.HTTPError as e:
                print(f"  Error en página {pagina} para '{keyword}': {e}")
                continue

            resultados = data.get("results", [])
            if not resultados:
                break  # no hay más páginas para esta keyword

            for oferta in resultados:
                todas_las_ofertas.append({
                    "keyword_busqueda": keyword,
                    "titulo": oferta.get("title"),
                    "empresa": oferta.get("company", {}).get("display_name"),
                    "ubicacion": oferta.get("location", {}).get("display_name"),
                    "descripcion": oferta.get("description"),
                    "salario_min": oferta.get("salary_min"),
                    "salario_max": oferta.get("salary_max"),
                    "fecha_creacion": oferta.get("created"),
                    "url": oferta.get("redirect_url"),
                })

            print(f"  Página {pagina}: {len(resultados)} ofertas recogidas")
            time.sleep(1)  # pausa para no saturar la API

    return todas_las_ofertas


if __name__ == "__main__":
    ofertas = recopilar_datos()
    df = pd.DataFrame(ofertas)

    # Eliminar duplicados por si una oferta sale en varias keywords
    df = df.drop_duplicates(subset=["titulo", "empresa", "url"])

    os.makedirs("data", exist_ok=True)
    ruta_salida = "data/ofertas_tech.csv"
    df.to_csv(ruta_salida, index=False, encoding="utf-8-sig")

    print(f"\n✅ Guardadas {len(df)} ofertas únicas en {ruta_salida}")