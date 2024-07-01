import streamlit as st

from src.pages.encuestas import Encuestas
from src.pages.respuestas import Respuestas
from src.pages.respuesta_especifica import RespuestaEspecifica
from src.utils.sidebar import sidebar_caption

# Basado en https://github.com/emptymalei/streamlit-multipage-template/tree/main

st.set_page_config(
    page_title="Dashboard Encuestas",
    page_icon="📊",
    initial_sidebar_state="expanded",
)

def main():
    st.sidebar.title("📃 Páginas")

    PAGES = {
        "📚 Encuestas": Encuestas,
        "📫 Respuestas": Respuestas,
        "📑 Respuesta Específica": RespuestaEspecifica,
    }

    # Select pages
    sidebar_caption()
    selection = st.sidebar.radio("", list(PAGES.keys()))
    st.sidebar.divider()
    st.sidebar.markdown("**Nota**")
    st.sidebar.markdown("*Seleccione solo opciones de la selección única*")

    page = PAGES[selection]

    DATA = None

    with st.spinner(f"Loading Page {selection} ..."):
        page = page(DATA)
        page()

if __name__ == "__main__":
    main()