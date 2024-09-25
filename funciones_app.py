import numpy as np
import pandas as pd
import streamlit as st
import math

import metodos_no_lineales

def biseccion_app(cols, error):
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

def regla_falsa_app(cols, error):
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

def secante_app(cols,error):
    col1, col2, col3, col4 = cols
    function = st.text_input('Ingrese la función a evaluar', value='np.exp(-x) + x**2 -13')
    function = eval(f'lambda x: {function}')
    with col1:
        x0 = st.number_input('Valor de x0', value=0)
    with col2:
        x1 = st.number_input('Valor de x1', value=5)
    with col3:
        tol = st.number_input('Tolerancia', value=0.0001)
    with col4:
        n = st.number_input('# Iteraciones', value=100)
    if x0 == x1:
        st.warning("x0 y x1 no pueden ser iguales")
        return
    if error == "Decimales Correctos":
        aprox, table = metodos_no_lineales.secante(function, x0, x1, tol, n)
        st.write(aprox)
        st.dataframe(table)
    else:
        aprox, table = metodos_no_lineales.secante(function, x0, x1, tol, n,True)
        st.write(aprox)
        st.dataframe(table)

def newton_app(cols, error):
    col1, col2, col3 = cols
    function = st.text_input('Ingrese la función a evaluar', value='math.exp(-x) + x**2 -13')
    function = eval(f'lambda x: {function}')
    with col1:
        x0 = st.number_input('Valor de x0',step=1.,format="%.3f", value=0.0)
    with col2:
        tol = st.number_input('Tolerancia', value=0.0001)
    with col3:
        n = st.number_input('# Iteraciones', value=100)

    if error == "Decimales Correctos":
        aprox, table = metodos_no_lineales.newton(function, x0, tol, n)
        st.write(aprox)
        st.dataframe(table)
    else:
        aprox, table = metodos_no_lineales.newton(function, x0, tol, n,True)
        st.write(aprox)
        st.dataframe(table)
def punto_fijo_app(cols, error):
    col1, col2, col3, col4 = cols
    function = st.text_input('Ingrese la función a evaluar', value='np.exp(-x) + x**2 -13')
    function = eval(f'lambda x: {function}')
    with col1:
        x0 = st.number_input('Valor de x0', value=0)
    with col2:
        g = st.text_input('Ingrese g(x)', value='np.exp(-x) + x**2 -13')
    g = eval(f'lambda x: {g}')
    with col3:
        tol = st.number_input('Tolerancia', value=0.0001)
    with col4:
        n = st.number_input('# Iteraciones', value=100)

    if error == "Decimales Correctos":
        aprox, table = metodos_no_lineales.punto_fijo(function, g,x0, tol, n)
        st.write(aprox)
        st.dataframe(table)
    else:
        aprox, table = metodos_no_lineales.secante(function, g,x0, tol, n,True)
        st.write(aprox)
        st.dataframe(table)

def raices_multiples2_app(cols, error):
    col1, col2, col3 = cols
    function = st.text_input('Ingrese la función a evaluar', value='math.exp(-x) + x**2 -13')
    function = eval(f'lambda x: {function}')
    with col1:
        x0 = st.number_input('Valor de x0',step=1.,format="%.3f", value=0.0)
    with col2:
        tol = st.number_input('Tolerancia', value=0.0001)
    with col3:
        n = st.number_input('# Iteraciones', value=100)

    if error == "Decimales Correctos":
        aprox, table = metodos_no_lineales.newton(function, x0, tol, n)
        st.write(aprox)
        st.dataframe(table)
    else:
        aprox, table = metodos_no_lineales.newton(function, x0, tol, n,True)
        st.write(aprox)
        st.dataframe(table)