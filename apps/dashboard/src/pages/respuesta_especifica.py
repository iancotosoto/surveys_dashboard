import streamlit as st

from src.utils.page import Page
from src.utils.response import manage_response, filtrar_datos
from src.utils.table import mostrar_tabla
from src.utils.diagrams import mostrar_graficos_barras

class RespuestaEspecifica(Page):

    def __init__(self, data, **kwargs):
        name = "📑 Respuestas específica"
        self.id_encuesta = 1
        super().__init__(name, data, **kwargs)

    # Métodos
    # Mostrar todo el contenido
    def content(self):
        # Mostrar contenido
        self.contenidoEntrada()  

        # Botón de búsqueda
        try:
            self.id_encuesta = int(self.id_encuesta)
            if st.button(label="Buscar"):
                with st.spinner('Buscando...'):
                    self.contenidoRespuestaEsp()
            else:
                st.write('Esperando a que se realice la búsqueda...')
        except Exception as e:
            st.write('Error:', str(e))

    # Mostrar contenido
    def contenidoEntrada(self):
        # Entrada de datos para buscar una encuesta específica
        st.subheader('Digite el número de encuesta')
        self.id_encuesta = st.text_input(label="Número de encuesta", value=1, label_visibility="collapsed")

    def contenidoRespuestaEsp(self):
        respuesta_esp_pd = manage_response(f'http://pyspark-app:8888/respuestas/{self.id_encuesta}')
        mostrar_tabla(f"Respuestas de encuesta #{self.id_encuesta}", respuesta_esp_pd)

        # Mostrar gráficos de barras para preguntas filtradas
        mostrar_graficos_barras(filtrar_datos(respuesta_esp_pd, 'Abiertas'))