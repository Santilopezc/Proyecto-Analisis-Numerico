import numpy as np
import pandas as pd
import streamlit as st
import math
import sympy as sp
from utils import display_result, get_derivative, get_second_derivative, graph, graph2, validar_numeros, graph_with_points

import metodos_no_lineales
import Sistemas_ecuaciones_numerico
import Funciones_Interpolacion

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
        x = sp.symbols('x')
        function = sp.lambdify(x, function_text)
        #function = eval(f'lambda x: {function_text}')
        test_value = function(0)  # Probar con un valor
        return function
    except SyntaxError:
        st.error("Error: La función ingresada tiene errores de sintaxis. Revísala.")
    except NameError as e:
        st.error(f"Error: Nombre desconocido en la función. Verifica que hayas escrito bien la funcion.")
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
    function = st.text_input('Ingrese la función a evaluar', value='exp(-x) + x**2 -13')
    og_function = function
    function = validar_funcion(function)
    if function:
        #function = eval(f'lambda x: {function}')
        with col1:
            a = st.number_input('Valor de a', step=1.,format="%.4f", value = 0.0)
        with col2:
            b = st.number_input('Valor de b', step=1.,format="%.4f", value = 5.0)
        with col3:
            n = st.number_input('# Iteraciones', value=100)
        if error == "Decimales Correctos":
            aprox, table = metodos_no_lineales.bisection(function, a, b, tol, n)
            display_result(aprox, table)
        else:
            aprox, table = metodos_no_lineales.bisection(function, a, b, tol, n,True)
            display_result(aprox, table)
        graph(sp.symbols('x'), og_function)

def regla_falsa_app(cols, error,tol):
    col1, col2, col3 = cols
    function = st.text_input('Ingrese la función a evaluar', value='exp(-x) + x**2 -13')
    og_function = function
    function = validar_funcion(function)
    if function:
        with col1:
            a = st.number_input('Valor de a', step=1.,format="%.4f", value = 0.0)
        with col2:
            b = st.number_input('Valor de b', step=1.,format="%.4f", value = 5.0)
        with col3:
            n = st.number_input('# Iteraciones', value=100)
        if error == "Decimales Correctos":
            aprox, table = metodos_no_lineales.regla_falsa(function, a, b, tol, n)
            display_result(aprox, table)
        else:
            aprox, table = metodos_no_lineales.regla_falsa(function, a, b, tol, n,True)
            display_result(aprox, table)
        graph(sp.symbols('x'), og_function)

def secante_app(cols,error, tol):
    col1, col2, col3 = cols
    function = st.text_input('Ingrese la función a evaluar', value='exp(-x) + x**2 -13')
    og_function = function
    function = validar_funcion(function)
    if function:
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
            display_result(aprox, table)
        else:
            aprox, table = metodos_no_lineales.secante(function, x0, x1, tol, n,True)
            display_result(aprox, table)
        graph(sp.symbols('x'), og_function)

def newton_app(cols, error, tol):
    # Revisar
    col1, col2 = cols
    function = st.text_input('Ingrese la función a evaluar', value='exp(-x) + x**2 -13')
    og_function = function
    derivada = get_derivative(function)
    function = validar_funcion(function)
    if function:
        with col1:
            x0 = st.number_input('Valor de x0',step=1.,format="%.4f", value=0.0)
        with col2:
            n = st.number_input('# Iteraciones', value=100)

        
        if error == "Decimales Correctos":
            aprox, table = metodos_no_lineales.newton(function, derivada, x0, tol, n)
            display_result(aprox, table)
        else:
            aprox, table = metodos_no_lineales.newton(function,derivada, x0, tol, n,True)
            display_result(aprox, table)
        graph(sp.symbols('x'), og_function)

def punto_fijo_app(cols, error, tol):
    col1, col2, col3 = cols
    function = st.text_input('Ingrese la función a evaluar', value='exp(-x) + x**2 -13')
    og_function = function
    function = validar_funcion(function)
    if function:
        with col1:
            x0 = st.number_input('Valor de x0',step=1.,format="%.4f", value = 0.0)
        with col2:
            g = st.text_input('Ingrese g(x)', value='exp(-x)')
        g = validar_funcion(g)
        if g:
            with col3:
                n = st.number_input('# Iteraciones', value=100)

            if error == "Decimales Correctos":
                aprox, table = metodos_no_lineales.punto_fijo(function, g,x0, tol, n)
                display_result(aprox, table)
            else:
                aprox, table = metodos_no_lineales.punto_fijo(function, g,x0, tol, n,True)
                display_result(aprox, table)
            graph(sp.symbols('x'), og_function)

def raices_multiples_app(cols, error, tol):
    col1, col2 = cols
    function = st.text_input('Ingrese la función a evaluar', value='exp(-x) + x**2 -13')
    og_function = function
    derivada = get_derivative(function)
    segunda_derivada = get_second_derivative(function)
    function = validar_funcion(function)
    if function:
        with col1:
            x0 = st.number_input('Valor de x0',step=1.,format="%.4f", value=0.0)
        with col2:
            n = st.number_input('# Iteraciones', value=100)

        if error == "Decimales Correctos":
            aprox, table = metodos_no_lineales.raices_multiples(function, derivada, segunda_derivada, x0, tol, n)
            display_result(aprox, table)
        else:
            aprox, table = metodos_no_lineales.raices_multiples(function, derivada, segunda_derivada, x0, tol, n,True)
            display_result(aprox, table)
        graph(sp.symbols('x'), og_function)


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
    if len(A.split(";")) == 2:
        for i in range(len(A.split(";"))):
            dim1 = len(A.split(";")[i].split())
           
        graph2(aprox,func1,func2, name1,name2 )      
   
        Am = np.array([list(map(float, row.split())) for row in A.split(';')])
        bm = np.array(list(map(float, b.split())))
        def func1(x): 
            if Am[0,1] == 0: 
                return(x*0 + bm[0]/Am[0,0])
            return((-Am[0,0]*x+bm[0])/Am[0,1])
        def func2(x): 
            if Am[1,1] == 0: 
                return(x*0+bm[1]/Am[1,0])
            return((-Am[1,0]*x+bm[1])/Am[1,1])
        name1 = f"y = ({-Am[0,0]}*x+{bm[0]})/{Am[0,1]}"
        name2 = f"y = ({-Am[1,0]}*x+{bm[1]})/{Am[1,1]}"
        graph2(aprox,func1,func2, name1,name2 )

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
    if len(A.split(";")) == 2:
        for i in range(len(A.split(";"))):
            dim1 = len(A.split(";")[i].split())
           
                
   
        Am = np.array([list(map(float, row.split())) for row in A.split(';')])
        bm = np.array(list(map(float, b.split())))
        def func1(x): 
            if Am[0,1] == 0: 
                return(x*0 + bm[0]/Am[0,0])
            return((-Am[0,0]*x+bm[0])/Am[0,1])
        def func2(x): 
            if Am[1,1] == 0: 
                return(x*0+bm[1]/Am[1,0])
            return((-Am[1,0]*x+bm[1])/Am[1,1])
        name1 = f"y = ({-Am[0,0]}*x+{bm[0]})/{Am[0,1]}"
        name2 = f"y = ({-Am[1,0]}*x+{bm[1]})/{Am[1,1]}"
        graph2(aprox,func1,func2, name1,name2 )
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
    if len(A.split(";")) == 2:
        for i in range(len(A.split(";"))):
            dim1 = len(A.split(";")[i].split())
           
                
   
        Am = np.array([list(map(float, row.split())) for row in A.split(';')])
        bm = np.array(list(map(float, b.split())))
        def func1(x): 
            if Am[0,1] == 0: 
                return(x*0 + bm[0]/Am[0,0])
            return((-Am[0,0]*x+bm[0])/Am[0,1])
        def func2(x): 
            if Am[1,1] == 0: 
                return(x*0+bm[1]/Am[1,0])
            return((-Am[1,0]*x+bm[1])/Am[1,1])
        name1 = f"y = ({-Am[0,0]}*x+{bm[0]})/{Am[0,1]}"
        name2 = f"y = ({-Am[1,0]}*x+{bm[1]})/{Am[1,1]}"
        graph2(aprox,func1,func2, name1,name2 )

def vandermonde_app(cols):
    col1, col2, col3 = cols
    with col1:
        x_str = st.text_input('Ingrese el vector de coeficientes de x (numeros con espacio, Filas separados por ;)', value="1 3 7")
    with col2:
        y_str = st.text_input('Ingrese el vector de coeficientes de y correspondientes con x (numeros con espacio, Filas separados por ;)', value="4 5 7")
    with col3:
        x_eval = st.text_input('Ingrese el valor de x a evaluar en el polinomio ', value = "3")

    polinomio_sim, polinomio_eval = Funciones_Interpolacion.polinomio_Vandermonde(x_str, y_str, x_eval)
    
    st.write("El polinomio interpolante es: " + str(polinomio_sim))
    st.write("El polinomio interpolante evaluado en "+str(x_eval)+" es: " + str(polinomio_sim))
    graph(sp.symbols('x'), polinomio_sim)

def polinomio_newton_app(cols):
    col1, col2 = cols
    with col1:
        x_str = st.text_input('Ingrese el vector de coeficientes de x (numeros con espacio, Filas separados por ;)', value="1 3 7")
    with col2:
        y_str = st.text_input('Ingrese el vector de coeficientes de y correspondientes con x (numeros con espacio, Filas separados por ;)', value="4 5 7")

    polinomio_sim, table = Funciones_Interpolacion.construir_polinomio_newton(x_str, y_str)

    st.write("El polinomio interpolante es: " + str(polinomio_sim))
    st.dataframe(table)
    graph(sp.symbols('x'), polinomio_sim)


def polinomio_lagrange_app(cols):
    col1, col2 = cols
    with col1:
        x_str = st.text_input('Ingrese el vector de coeficientes de x (numeros con espacio, Filas separados por ;)', value="1 3 7")
    with col2:
        y_str = st.text_input('Ingrese el vector de coeficientes de y correspondientes con x (numeros con espacio, Filas separados por ;)', value="4 5 7")

    polinomio_sim = Funciones_Interpolacion.polinomio_lagrange(x_str, y_str)

    st.write("El polinomio interpolante es: " + str(polinomio_sim))
    graph(sp.symbols('x'), polinomio_sim)

def spline_cuadratico_app(cols):
    col1, col2 = cols
    with col1:
        x_str = st.text_input('Ingrese el vector de coeficientes de x (numeros con espacio, Filas separados por ;)', value="1 3 7")
    with col2:
        y_str = st.text_input('Ingrese el vector de coeficientes de y correspondientes con x (numeros con espacio, Filas separados por ;)', value="4 5 7")

    polinomio_sim = Funciones_Interpolacion.spline_cuadratico(x_str, y_str)

    st.write("Los polinomios interpolantes para cada intervalo son: " + str(polinomio_sim))


def spline_lineal_app(cols):
    col1, col2, col3 = cols
    with col1:
        x_str = validar_numeros(st.text_input('Ingrese el vector de coeficientes de x (numeros con espacio, Filas separados por ;)', value="1 3 7"))
    with col2:
        y_str = st.text_input('Ingrese el vector de coeficientes de y correspondientes con x (numeros con espacio, Filas separados por ;)', value="4 5 7")
    with col3:
        x_eval = st.text_input('Ingrese el valor de x a evaluar en el polinomio ', value = "3")

    polinomio_sim, polinomio_eval = Funciones_Interpolacion.spline_lineal(x_str, y_str, x_eval)
    
    st.write("Los polinomios interpolantes para cada intervalo son: " + str(polinomio_sim))
    if isinstance(polinomio_eval, str):
        st.write("El polinomio interpolante evaluado en "+str(x_eval)+" es: " + (polinomio_eval))
    else:
        st.write("El polinomio interpolante evaluado en "+str(x_eval)+" es: " + str(polinomio_eval))
















