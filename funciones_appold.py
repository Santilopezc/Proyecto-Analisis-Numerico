import numpy as np
import pandas as pd
import streamlit as st
import math

import metodos_no_lineales
import Sistemas_ecuaciones_numerico


def biseccion_app(cols, error,tol):
    col1, col2, col3 = cols
    function = st.text_input('Ingrese la función a evaluar', value='np.exp(-x) + x**2 -13')
    function = eval(f'lambda x: {function}')
    with col1:
        a = st.number_input('Valor de a', step=1.,format="%.4f", value = 0.0)
    with col2:
        b = st.number_input('Valor de b', step=1.,format="%.4f", value = 5.0)
    with col3:
        n = st.number_input('# Iteraciones', value=100)
    if error == "Decimales Correctos":
        aprox, table = metodos_no_lineales.bisection(function, a, b, tol, n)
        st.write(aprox)
        st.dataframe(table)
    else:
        aprox, table = metodos_no_lineales.bisection(function, a, b, tol, n,True)
        st.write(aprox)
        st.dataframe(table)

def regla_falsa_app(cols, error,tol):
    col1, col2, col3 = cols
    function = st.text_input('Ingrese la función a evaluar', value='np.exp(-x) + x**2 -13')
    function = eval(f'lambda x: {function}')
    with col1:
        a = st.number_input('Valor de a', step=1.,format="%.4f", value = 0.0)
    with col2:
        b = st.number_input('Valor de b', step=1.,format="%.4f", value = 5.0)
    with col3:
        n = st.number_input('# Iteraciones', value=100)
    if error == "Decimales Correctos":
        aprox, table = metodos_no_lineales.regla_falsa(function, a, b, tol, n)
        st.write(aprox)
        st.dataframe(table)
    else:
        aprox, table = metodos_no_lineales.regla_falsa(function, a, b, tol, n,True)
        st.write(aprox)
        st.dataframe(table)

def secante_app(cols,error, tol):
    col1, col2, col3 = cols
    function = st.text_input('Ingrese la función a evaluar', value='np.exp(-x) + x**2 -13')
    function = eval(f'lambda x: {function}')
    with col1:
        x0 = st.number_input('Valor de x0',step=1.,format="%.4f", value = 0.0)
    with col2:
        x1 = st.number_input('Valor de x1', step=1.,format="%.4f", value = 5.0)
    with col3:
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

def newton_app(cols, error, tol):
    col1, col2 = cols
    function = st.text_input('Ingrese la función a evaluar', value='math.exp(-x) + x**2 -13')
    function = eval(f'lambda x: {function}')
    with col1:
        x0 = st.number_input('Valor de x0',step=1.,format="%.4f", value=0.0)
    with col2:
        n = st.number_input('# Iteraciones', value=100)

    if error == "Decimales Correctos":
        aprox, table = metodos_no_lineales.newton(function, x0, tol, n)
        st.write(aprox)
        st.dataframe(table)
    else:
        aprox, table = metodos_no_lineales.newton(function, x0, tol, n,True)
        st.write(aprox)
        st.dataframe(table)

def punto_fijo_app(cols, error, tol):
    col1, col2, col3 = cols
    function = st.text_input('Ingrese la función a evaluar', value='np.exp(-x) + x**2 -13')
    function = eval(f'lambda x: {function}')
    with col1:
        x0 = st.number_input('Valor de x0',step=1.,format="%.4f", value = 0.0)
    with col2:
        g = st.text_input('Ingrese g(x)', value='np.exp(-x) + x**2 -13')
    g = eval(f'lambda x: {g}')
    with col3:
        n = st.number_input('# Iteraciones', value=100)

    if error == "Decimales Correctos":
        aprox, table = metodos_no_lineales.punto_fijo(function, g,x0, tol, n)
        st.write(aprox)
        st.dataframe(table)
    else:
        aprox, table = metodos_no_lineales.punto_fijo(function, g,x0, tol, n,True)
        st.write(aprox)
        st.dataframe(table)

def raices_multiples2_app(cols, error, tol):
    col1, col2 = cols
    function = st.text_input('Ingrese la función a evaluar', value='math.exp(-x) + x**2 -13')
    function = eval(f'lambda x: {function}')
    with col1:
        x0 = st.number_input('Valor de x0',step=1.,format="%.4f", value=0.0)
    with col2:
        n = st.number_input('# Iteraciones', value=100)

    if error == "Decimales Correctos":
        aprox, table = metodos_no_lineales.raices_multiples2(function, x0, tol, n)
        st.write(aprox)
        st.dataframe(table)
    else:
        aprox, table = metodos_no_lineales.raices_multiples2(function, x0, tol, n,True)
        st.write(aprox)
        st.dataframe(table)

def jacobi_app(cols, error, tol):
    col1, col2 = cols
    with col1:
        A = st.text_input('Ingrese la matriz de coeficientes (numeros con espacio, Filas separados por ;)', value="3 0 2; 2 6 2; 7 0 9")
        n = st.number_input('# Iteraciones', value=100)
    if error != "Decimales Correctos":
        error = st.selectbox("Calculo del Error Relativo",("Norma infinito de división vectorial","División de normas infinito"))
    with col2:
        X_0 = st.text_input('Ingrese los valores iniciales (separar numeros por espacio)', value = "1 2 3")
        b = st.text_input('Ingrese el vector de resultados (separar numeros por espacio)', value = "10 10 10")

    if error == "Decimales Correctos":
        aprox, table, radio = Sistemas_ecuaciones_numerico.Jacobi(A,b,X_0,tol,n)
        st.write(aprox)
        st.write("El radio espectral de la matriz de transformación es: " + str(radio))
        st.dataframe(table)
    elif error == "Norma infinito de división vectorial":
        aprox, table, radio = Sistemas_ecuaciones_numerico.Jacobi(A,b,X_0, tol, n,1)
        st.write(aprox)
        st.write("El radio espectral de la matriz de transformación es: " + str(radio))
        st.dataframe(table)
    else:
        aprox, table, radio = Sistemas_ecuaciones_numerico.Jacobi(A,b,X_0, tol, n,2)
        st.write(aprox)
        st.write("El radio espectral de la matriz de transformación es: " + str(radio))
        st.dataframe(table)  

def gauss_seidel_app(cols, error, tol):
    col1, col2 = cols
    with col1:
        A = st.text_input('Ingrese la matriz de coeficientes (numeros con espacio, Filas separados por ;)', value="3 0 2; 2 6 2; 7 0 9")
        n = st.number_input('# Iteraciones', value=100)
    if error != "Decimales Correctos":
        error = st.selectbox("Calculo del Error Relativo",("Norma infinito de división vectorial","División de normas infinito"))
    with col2:
        X_0 = st.text_input('Ingrese los valores iniciales (separar numeros por espacio)', value = "1 2 3")
        b = st.text_input('Ingrese el vector de resultados (separar numeros por espacio)', value = "10 10 10")

    if error == "Decimales Correctos":
        aprox, table, radio = Sistemas_ecuaciones_numerico.Gauss_Seidel(A,b,X_0,tol,n)
        st.write(aprox)
        st.write("El radio espectral de la matriz de transformación es: " + str(radio))
        st.dataframe(table)
    elif error == "Norma infinito de división vectorial":
        aprox, table, radio = Sistemas_ecuaciones_numerico.Gauss_Seidel(A,b,X_0, tol, n,1)
        st.write(aprox)
        st.write("El radio espectral de la matriz de transformación es: " + str(radio))
        st.dataframe(table)
    else:
        aprox, table, radio = Sistemas_ecuaciones_numerico.Gauss_Seidel(A,b,X_0, tol, n,2)
        st.write(aprox)
        st.write("El radio espectral de la matriz de transformación es: " + str(radio))
        st.dataframe(table)  
def SOR_app(cols, error, tol):
    col1, col2 = cols
    with col1:
        A = st.text_input('Ingrese la matriz de coeficientes (numeros con espacio, Filas separados por ;)', value="3 0 2; 2 6 2; 7 0 9")
        n = st.number_input('# Iteraciones', value=100)
        w = st.number_input('Parámetro de Relajación', value=1.0, min_value = 0.0, max_value = 2.0, step = 0.1)
    with col2:
        X_0 = st.text_input('Ingrese los valores iniciales (separar numeros por espacio)', value = "1 2 3")
        b = st.text_input('Ingrese el vector de resultados (separar numeros por espacio)', value = "10 10 10")
    if error != "Decimales Correctos":
        error = st.selectbox("Calculo del Error Relativo",("Norma infinito de división vectorial","División de normas infinito"))
    if error == "Decimales Correctos":
        aprox, table, radio = Sistemas_ecuaciones_numerico.SOR(A,b,X_0,tol,n,w)
        st.write(aprox)
        st.write("El radio espectral de la matriz de transformación es: " + str(radio))
        st.dataframe(table)
    elif error == "Norma infinito de división vectorial":
        aprox, table, radio = Sistemas_ecuaciones_numerico.SOR(A,b,X_0, tol, n,w,1)
        st.write(aprox)
        st.write("El radio espectral de la matriz de transformación es: " + str(radio))
        st.dataframe(table)
    else:
        aprox, table, radio = Sistemas_ecuaciones_numerico.SOR(A,b,X_0, tol, n,w,2)
        st.write(aprox)
        st.write("El radio espectral de la matriz de transformación es: " + str(radio))
        st.dataframe(table)  
    
