import os
import re
import pandas as pd

RUTA_ENTRADA = "data/ofertas_tech.csv"
RUTA_SALIDA_DETALLE = "data/ofertas_con_skills.csv"
RUTA_SALIDA_RESUMEN = "data/resumen_skills.csv"

# Diccionario de skills a detectar.
# La clave es el nombre "bonito" que se mostrará, el valor es una lista de
# variantes/alias que pueden aparecer en el texto (todo en minúsculas).
SKILLS = {
    "Python": ["python"],
    "Java": [r"\bjava\b"],
    "JavaScript": ["javascript", "js "],
    "HTML/CSS": ["html", "css"],
    "SQL": [r"\bsql\b", "mysql", "postgresql", "postgres", "sql server", "t-sql", "pl/sql"],
    "Docker": ["docker"],
    "Kubernetes": ["kubernetes", r"\bk8s\b"],
    "AWS": [r"\baws\b", "amazon web services"],
    "Azure": ["azure"],
    "GCP": [r"\bgcp\b", "google cloud"],
    "React": ["react"],
    "Machine Learning": ["machine learning", r"\bml\b"],
    "TensorFlow": ["tensorflow"],
    "PyTorch": ["pytorch"],
    "Pandas": ["pandas"],
    "Git": [r"\bgit\b"],
    "Linux": ["linux"],
    "Agile/Scrum": ["agile", "scrum"],
    "Django": ["django"],
    "Flask": ["flask"],
    "Node.js": ["node.js", "nodejs", r"\bnode\b"],
}


def detectar_skills(texto):
    """Devuelve la lista de skills detectadas en un texto dado."""
    if not isinstance(texto, str):
        return []

    texto_lower = texto.lower()
    encontradas = []

    for skill, patrones in SKILLS.items():
        for patron in patrones:
            if re.search(patron, texto_lower):
                encontradas.append(skill)
                break  # ya encontramos esta skill, no hace falta seguir

    return encontradas


def procesar():
    if not os.path.exists(RUTA_ENTRADA):
        print(f"No se encuentra {RUTA_ENTRADA}. Ejecuta primero scraper.py")
        return

    df = pd.read_csv(RUTA_ENTRADA)

    # Detectar skills combinando título + descripción
    df["skills_detectadas"] = (
        df["titulo"].fillna("") + " " + df["descripcion"].fillna("")
    ).apply(detectar_skills)

    df["num_skills"] = df["skills_detectadas"].apply(len)

    # Guardar el detalle (skills como lista separada por comas, más legible en CSV)
    df_guardar = df.copy()
    df_guardar["skills_detectadas"] = df_guardar["skills_detectadas"].apply(
        lambda lista: ", ".join(lista)
    )
    df_guardar.to_csv(RUTA_SALIDA_DETALLE, index=False, encoding="utf-8-sig")
    print(f"✅ Detalle guardado en {RUTA_SALIDA_DETALLE} ({len(df_guardar)} ofertas)")

    # Generar resumen: cuántas ofertas mencionan cada skill
    conteo = {}
    for lista_skills in df["skills_detectadas"]:
        for skill in lista_skills:
            conteo[skill] = conteo.get(skill, 0) + 1

    df_resumen = (
        pd.DataFrame(list(conteo.items()), columns=["skill", "num_ofertas"])
        .sort_values("num_ofertas", ascending=False)
        .reset_index(drop=True)
    )
    df_resumen["porcentaje"] = (
        df_resumen["num_ofertas"] / len(df) * 100
    ).round(1)

    df_resumen.to_csv(RUTA_SALIDA_RESUMEN, index=False, encoding="utf-8-sig")
    print(f"✅ Resumen guardado en {RUTA_SALIDA_RESUMEN}")
    print("\nTop 10 skills más demandadas:")
    print(df_resumen.head(10).to_string(index=False))


if __name__ == "__main__":
    procesar()