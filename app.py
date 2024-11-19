import streamlit as st
import pandas as pd
import numpy as np
import funciones_app
import math

st.title('Metodos Numericos')

col1, col2= st.columns([1,1])

with col1:
    error = st.selectbox(
    "Quieres utilizar Cifras Significativas o Decimales Correctos?",
    ("Decimales Correctos", "Cifras Significativas"),
)

with col2:
    decimals = st.number_input(f'Ingrese el número de {error}', min_value=1, max_value=10, value=3)

if error == "Decimales Correctos":
    tol = 0.5 * 10 ** (-decimals)
else:
    tol = 5 * 10 ** (-decimals)

method = st.selectbox(
"Que metodo quieres utilizar?",
("Biseccion", "Regla Falsa", "Secante", "Newton", "Punto Fijo", "Raices Multiples", "Jacobi", "Gauss_Seidel", "SOR", "Vandermonde", "Polinomio_Newton", 
 "Polinomio_Lagrange", "Spline_Cuadratico", "Spline_Lineal"),)

methods = {
    "Biseccion": funciones_app.biseccion_app,
    "Regla Falsa": funciones_app.regla_falsa_app,
    "Secante": funciones_app.secante_app,
    "Newton": funciones_app.newton_app,
    "Punto Fijo": funciones_app.punto_fijo_app,
    "Raices Multiples":funciones_app.raices_multiples_app,
    "Jacobi":funciones_app.jacobi_app,
    "Gauss_Seidel":funciones_app.gauss_seidel_app,
    "SOR":funciones_app.SOR_app,
    "Vandermonde":funciones_app.vandermonde_app,
    "Polinomio_Newton":funciones_app.polinomio_newton_app,
    "Polinomio_Lagrange":funciones_app.polinomio_lagrange_app,
    "Spline_Cuadratico":funciones_app.spline_cuadratico_app,
    "Spline_Lineal":funciones_app.spline_lineal_app
}
if method in ["Biseccion", "Regla Falsa", "Secante", "Punto Fijo", "Vandermonde", "Spline_Lineal"]:
    cols = st.columns([1,1,1])
if method in ["Newton",  "Raices Multiples", "Polinomio_Newton", "Polinomio_Lagrange", "Spline_Cuadratico"]:
    cols = st.columns([1,1])
if method in ["Jacobi", "Gauss_Seidel", "SOR"]:
    cols = st.columns([1,1])
    
if method in ["Vandermonde", "Spline_Lineal", "Polinomio_Newton", "Polinomio_Lagrange", "Spline_Cuadratico"]:
    methods[method](cols)
else:
    methods[method](cols, error,tol)

