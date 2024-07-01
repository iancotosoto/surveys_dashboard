import streamlit as st

from src.utils.response import manage_response

# Función auxiliar para obtener datos desde una URL
def obtener_datos(url):
    return manage_response(url)

# Función auxiliar para mostrar DataFrame en Streamlit
def mostrar_tabla(titulo, df):
    if df.empty:
        st.warning('No hay datos para mostrar.')
        return
    st.markdown("**" + titulo + "**")
    st.write(df)