import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Radar de Empleo Tech",
    page_icon="📊",
    layout="wide",
)

RUTA_OFERTAS = "data/ofertas_con_skills.csv"
RUTA_RESUMEN = "data/resumen_skills.csv"


@st.cache_data
def cargar_datos():
    ofertas = pd.read_csv(RUTA_OFERTAS)
    resumen = pd.read_csv(RUTA_RESUMEN)
    return ofertas, resumen


ofertas, resumen = cargar_datos()

st.title("📊 Radar de Empleo Tech")
st.markdown(
    "Análisis de ofertas de empleo tech en España: skills más demandadas "
    "según datos reales extraídos de la API de Adzuna."
)

# --- Métricas generales ---
col1, col2, col3 = st.columns(3)
col1.metric("Ofertas analizadas", f"{len(ofertas):,}")
col2.metric("Skills distintas detectadas", len(resumen))
col3.metric("Skill más demandada", resumen.iloc[0]["skill"])

st.divider()

# --- Gráfico de skills más demandadas ---
st.subheader("Skills más demandadas")

top_n = st.slider("Número de skills a mostrar", 5, len(resumen), 10)

st.bar_chart(
    resumen.head(top_n).set_index("skill")["num_ofertas"],
    horizontal=True,
)

st.divider()

# --- Tabla explorable de ofertas ---
st.subheader("Explorar ofertas")

skills_disponibles = sorted(resumen["skill"].unique())
skill_filtro = st.multiselect(
    "Filtrar por skill",
    skills_disponibles,
)

ofertas_filtradas = ofertas
if skill_filtro:
    ofertas_filtradas = ofertas[
        ofertas["skills_detectadas"].fillna("").apply(
            lambda s: any(skill in s for skill in skill_filtro)
        )
    ]

st.write(f"Mostrando {len(ofertas_filtradas)} ofertas")
st.dataframe(
    ofertas_filtradas[
        ["titulo", "empresa", "ubicacion", "skills_detectadas", "fecha_creacion", "url"]
    ],
    use_container_width=True,
    hide_index=True,
)