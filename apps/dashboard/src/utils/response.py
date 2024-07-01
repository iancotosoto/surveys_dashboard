import streamlit as st
import pandas as pd
from src.utils.requester import request_data

# Función para filtrar datos según categoría
def filtrar_datos(df, categoria_excluir):
    return df[df['CategoriaPregunta'] != categoria_excluir] if not df.empty else df

# Función para manejar la respuesta de la API
def manage_response(url: str) -> pd.DataFrame:
    with st.spinner('Buscando...'):
        try:
            data = request_data(url)
            if data['status'] == 'success':
                data = pd.DataFrame(data['data'])
            else:
                data = pd.DataFrame({"Error": data['message']})
        except Exception as e:
            data = pd.DataFrame({"Error": str(e)})
        finally:
            return data