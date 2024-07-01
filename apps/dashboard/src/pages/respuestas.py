import streamlit as st

from src.utils.page import Page
from src.utils.response import manage_response, filtrar_datos
from src.utils.table import mostrar_tabla
from src.utils.diagrams import mostrar_graficos_barras

class Respuestas(Page):

    def __init__(self, data, **kwargs):
        name = "📫 Respuestas"
        self.id_encuesta = 1
        super().__init__(name, data, **kwargs)

    # Métodos
    # Mostrar todo el contenido
    def content(self):
        # Mostrar contenido
        self.contenidoRepuestas()
        
    # Mostrar contenido
    def contenidoRepuestas(self):
        # Cargar datos de respuestas
        respuestas_pd = manage_response('http://pyspark-app:8888/respuestas')
        mostrar_tabla("Respuestas de encuestas", respuestas_pd)

        # Mostrar gráficos de barras para preguntas filtradas
        mostrar_graficos_barras(filtrar_datos(respuestas_pd, 'Abiertas'))