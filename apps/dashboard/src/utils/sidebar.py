import streamlit as st

def sidebar_caption():
    st.sidebar.markdown("*Escoger una página para mostrar datos*")

def filter_table_option():

    show_n_records = st.sidebar.slider('Show how many', 0, 30, 1)

    return show_n_records