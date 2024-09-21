import streamlit as st
import pandas as pd
import numpy as np
from funciones_interfaz import biseccion_interfaz, regla_falsa_interfaz

st.title('Metodos Numericos')

col1, col2= st.columns([1,1])

with col1:
    error = st.selectbox(
    "Quieres utilizar Cifras Significativas o Decimales Correctos?",
    ("Decimales Correctos", "Cifras Significatias"),
)
with col2:
    decimals = st.number_input(f'Ingrese el número de {error}', min_value=1, max_value=10, value=3)
method = st.selectbox(
"Que metodo quieres utilizar?",
("Biseccion", "Regla Falsa"),)

cols = st.columns([1,1,1,1])
if method == "Biseccion":
    biseccion_interfaz(cols,error)
elif method == "Regla Falsa":
    regla_falsa_interfaz(cols, error)
