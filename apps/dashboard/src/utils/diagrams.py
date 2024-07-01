import streamlit as st
import matplotlib.pyplot as plt

# Función para mostrar gráficos de barras para cada grupo de encuestas y preguntas
def mostrar_graficos_barras(df_filtrado):
    if df_filtrado.empty:
        st.warning('No hay datos para mostrar.')
        return
    for numero_encuesta, encuesta_group in df_filtrado.groupby('NumeroEncuesta'):
        st.subheader(f'Encuesta {numero_encuesta}')
        for numero_pregunta, pregunta_group in encuesta_group.groupby('NumeroPregunta'):
            titulo = f'#{numero_pregunta}: Pregunta {pregunta_group["Pregunta"].iloc[0]} ({pregunta_group["CategoriaPregunta"].iloc[0]})'
            crear_grafico_barras(pregunta_group, x_col='Respuesta', y_col='CantidadRespuestas', 
                                titulo=titulo, color='#7469B6')
    

# Función auxiliar para crear gráficos de barras
def crear_grafico_barras(df, x_col, y_col, titulo, color="#63ECBB", width=50, height=400):
    if len(df) <= 0:
        st.warning('No hay datos para mostrar.')
        return
    st.text(titulo)
    st.bar_chart(data=df, x=x_col, y=y_col, color=color, width=width, height=height)

# Función auxiliar para crear gráficos de pastel
def crear_grafico_pastel(df, labels_col, values_col, titulo, colores, texto_color="white", fondo_color="#0E1118"):
    if len(df) <= 0:
        st.warning('No hay datos para mostrar.')
        return
    fig = plt.figure()
    explode = [0.1, 0] if len(df) == 2 else [0]  # Configuración de separación de las porciones del pastel
    plt.pie(df[values_col], explode=explode, labels=df[labels_col], colors=colores,
            autopct='%1.1f%%', textprops={'color': texto_color}, wedgeprops={'edgecolor': texto_color})
    plt.title(titulo, color=texto_color, fontsize=14, fontweight='bold')
    fig.patch.set_facecolor(fondo_color)
    st.pyplot(fig)