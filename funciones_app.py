import numpy as np
import pandas as pd
import streamlit as st
import math

import metodos_no_lineales
import Sistemas_ecuaciones_numerico

def mostrar_ayuda():
    st.sidebar.markdown("## Ayuda General")
    with st.sidebar.expander("Formato de entrada para funciones"):
        st.write("""
        - *Potencias*: Usa ** en lugar de ^. Ejemplo: \(x^2\) → x**2.
        - *Funciones especiales*: Usa np.exp, np.sin, np.log, etc.
        - *Ejemplos*:
            - \(e^{-x} + x^2 - 13\) → np.exp(-x) + x**2 - 13
            - \(\sin(x) - x/2\) → np.sin(x) - x/2
        - *Constantes*:
            - Usa np.pi para π, np.e para \(e\).
        """)
    with st.sidebar.expander("Errores comunes"):
        st.write("""
        - *Función mal ingresada*: No olvides el prefijo np. para funciones como exp o sin.
        - *Omitir paréntesis*: \(2x\) → 2*x.
        - *Intervalo inválido (bisección)*: Asegúrate de que \(f(a)\) y \(f(b)\) tengan signos opuestos.
        - *Matrices*: La matriz \(A\) debe ser cuadrada y compatible con el vector \(b\).
        """)


def validar_funcion(function_text):
    """Validar que la función sea válida y retornar una función evaluable."""
    try:
        function = eval(f'lambda x: {function_text}')
        test_value = function(0)  # Probar con un valor
        return function
    except SyntaxError:
        st.error("Error: La función ingresada tiene errores de sintaxis. Revísala.")
    except NameError as e:
        st.error(f"Error: Nombre desconocido en la función. Verifica que usas np. para funciones especiales.")
    except Exception as e:
        st.error(f"Error en la función: {e}.")
    return None


def validar_intervalo(function, a, b):
    """Validar que el intervalo sea válido para métodos de raíces."""
    try:
        fa, fb = function(a), function(b)
        if fa * fb > 0:
            st.warning("Error: Los valores de f(a) y f(b) tienen el mismo signo. Elige otro intervalo.")
            return False
        return True
    except Exception as e:
        st.error(f"Error al evaluar la función en el intervalo: {e}")
        return False


def validar_matriz(A_text, b_text):
    """Validar que la matriz y el vector sean compatibles y retornarlos."""
    try:
        A = np.array([list(map(float, row.split())) for row in A_text.split(';')])
        b = np.array(list(map(float, b_text.split())))
        if A.shape[0] != A.shape[1]:
            st.error("Error: La matriz debe ser cuadrada.")
            return None, None
        if A.shape[0] != b.shape[0]:
            st.error("Error: El número de filas en A debe coincidir con el tamaño del vector b.")
            return None, None
        return A, b
    except ValueError:
        st.error("Error: No se pudo convertir los datos ingresados. Verifica el formato.")
        return None, None

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
