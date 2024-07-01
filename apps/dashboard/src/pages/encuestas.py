import seaborn as sns

from src.utils.page import Page
from src.utils.response import manage_response
from src.utils.table import mostrar_tabla
from src.utils.diagrams import crear_grafico_barras, crear_grafico_pastel

class Encuestas(Page):

    def __init__(self, data, **kwargs):
        name = "📚 Encuestas"
        super().__init__(name, data, **kwargs)

    # Métodos
    # Mostrar todo el contenido
    def content(self):
        self.contenidoAutores()
        self.contenidoDisponibles()
        self.contenidoCategorias()
        self.contenidoPreguntas()
        self.contenidoRespuestas()

    # Mostrar contenido de autores
    def contenidoAutores(self):
        autores_pd = manage_response('http://pyspark-app:8888/encuestas/cantidad/autores')
        mostrar_tabla("Cantidad de encuestas por autor", autores_pd)
        crear_grafico_barras(autores_pd, x_col="Autor", y_col="CantidadEncuestas", titulo="Diagrama")

    # Mostrar contenido de encuestas disponibles
    def contenidoDisponibles(self):
        disponibles_pd = manage_response('http://pyspark-app:8888/encuestas/cantidad/disponibles')
        disponible_map = {1: "Disponible", 0: "Indisponible"}
        disponibles_pd["Disponible"] = disponibles_pd["Disponible"].map(disponible_map)
        disponibles_pd.rename(columns={"CantidadEncuestas": "Cantidad", "Disponible": "Estado"}, inplace=True)
        disponibles_pd = disponibles_pd[["Estado", "Cantidad"]].sort_values(by="Cantidad", ascending=False)
        mostrar_tabla("Cantidad de encuestas disponibles e indisponibles", disponibles_pd)
        colores = sns.color_palette("Greens", n_colors=len(disponibles_pd["Cantidad"]))
        crear_grafico_pastel(disponibles_pd, labels_col="Estado", values_col="Cantidad", titulo='Estado de las encuestas', colores=colores)

    # Mostrar contenido de categorías
    def contenidoCategorias(self):
        categorias_pd = manage_response('http://pyspark-app:8888/encuestas/cantidad/categorias')
        categorias_pd.rename(columns={"CantidadPreguntas": "Cantidad"}, inplace=True)
        mostrar_tabla("Cantidad de encuestas por categoría", categorias_pd)
        crear_grafico_barras(categorias_pd, x_col="Categoria", y_col="Cantidad", titulo="Diagrama")

    # Mostrar contenido de preguntas
    def contenidoPreguntas(self):
        preguntas_pd = manage_response('http://pyspark-app:8888/encuestas/cantidad/preguntas')
        preguntas_pd.rename(columns={"CantidadPreguntas": "Cantidad", "NumeroEncuesta": "Encuesta"}, inplace=True)
        mostrar_tabla("Cantidad de preguntas por encuesta", preguntas_pd)
        crear_grafico_barras(preguntas_pd, x_col="Encuesta", y_col="Cantidad", titulo="Diagrama")

    # Mostrar contenido de respuestas
    def contenidoRespuestas(self):
        respuestas_pd = manage_response('http://pyspark-app:8888/encuestas/cantidad/respuestas')
        respuestas_pd.rename(columns={"CantidadRespuestas": "Cantidad", "NumeroEncuesta": "Encuesta"}, inplace=True)
        mostrar_tabla("Cantidad de respuestas por encuesta", respuestas_pd)
        crear_grafico_barras(respuestas_pd, x_col="Encuesta", y_col="Cantidad", titulo="Diagrama")