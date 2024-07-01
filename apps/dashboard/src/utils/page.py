import streamlit as st

class Page:
    def __init__(self, name, data, **kwargs):
        self.name = name
        self.data = data
        self.kwargs = kwargs

    def content(self):
        raise NotImplementedError("Please implement this method.")

    def title(self):
        st.title(f"{self.name}")

    def __call__(self):
        self.title()
        self.content()