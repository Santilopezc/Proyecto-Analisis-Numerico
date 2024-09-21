import numpy as np
import pandas as pd
import streamlit as st

import metodos_no_lineales

def biseccion_interfaz(cols, error):
    col1, col2, col3, col4 = cols
    function = st.text_input('Ingrese la función a evaluar', value='np.exp(-x) + x**2 -13')
    function = eval(f'lambda x: {function}')
    with col1:
        a = st.number_input('Valor de a', value=0)
    with col2:
        b = st.number_input('Valor de b', value=5)
    with col3:
        tol = st.number_input('Tolerancia', value=0.0001)
    with col4:
        n = st.number_input('# Iteraciones', value=100)
    if error == "Decimales Correctos":
        aprox, table = metodos_no_lineales.bisection(function, a, b, tol, n)
        st.write(aprox)
        st.dataframe(table)
    else:
        aprox, table = metodos_no_lineales.bisection(function, a, b, tol, n,True)
        st.write(aprox)
        st.dataframe(table)

def regla_falsa_interfaz(cols, error):
    col1, col2, col3, col4 = cols
    function = st.text_input('Ingrese la función a evaluar', value='np.exp(-x) + x**2 -13')
    function = eval(f'lambda x: {function}')
    with col1:
        a = st.number_input('Valor de a', value=0)
    with col2:
        b = st.number_input('Valor de b', value=5)
    with col3:
        tol = st.number_input('Tolerancia', value=0.0001)
    with col4:
        n = st.number_input('# Iteraciones', value=100)
    if error == "Decimales Correctos":
        aprox, table = metodos_no_lineales.regla_falsa(function, a, b, tol, n)
        st.write(aprox)
        st.dataframe(table)
    else:
        aprox, table = metodos_no_lineales.regla_falsa(function, a, b, tol, n,True)
        st.write(aprox)
        st.dataframe(table)