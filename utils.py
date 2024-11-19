import pandas as pd
import streamlit as st
import sympy as sp
import plotly.graph_objs as go
import plotly.io as pio
import os
import numpy as np

def calculate_error(use_sig_digits: bool, x_m: float, x_list: list, index: int):
    if use_sig_digits:
        error = abs((x_m - x_list[index-1]) / x_m)
    else:
        error = abs(x_m - x_list[index-1])
    return error

def make_table(x_m_list, f_list, errors):
    table = pd.DataFrame({
        'X_m': x_m_list,
        'f(X_m)': f_list,
        'Error': errors
    })
    return table

def display_result(aprox, table):
    if aprox is None and table is None:
        return
    st.write(aprox)
    st.dataframe(table)
    return

def get_derivative(f):
    x = sp.symbols('x')
    f_prime = sp.diff(f, x)
    f_prime = sp.lambdify(x, f_prime)
    return f_prime
def get_second_derivative(f):
    x = sp.symbols('x')
    f_prime = sp.diff(f, x)
    f_prime2 = sp.diff(f_prime, x)
    f_prime2 = sp.lambdify(x, f_prime2)
    return f_prime2
def graph(x, function_input):

    # Create a symbolic function
    function = sp.lambdify(x, function_input, 'numpy')

    col7, col8 = st.columns(2)
    with col7:
        x_min = st.number_input(f"Enter the minimum value for {x}", value=0, step=1)
    with col8:
        x_max = st.number_input(f"Enter the maximum value for {x}", value=10, step=1)

    x_vals = np.linspace(x_min, x_max, 1000)
    y_vals = function(x_vals)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', name= str(function_input)))

    fig.update_layout(
        title=f"Graph of {function_input}",
        xaxis_title=str(x),
        yaxis_title=f"f({str(x)})",
        showlegend=True,
        margin=dict(l=0, r=0, t=40, b=0),
        hovermode="closest"
    )

    st.plotly_chart(fig)

    svg_file = "function_graph.svg"
    pio.write_image(fig, svg_file, format='svg', engine='kaleido')
    # Check if the SVG file was created
    try:
        with open(svg_file, "rb") as file:
            st.download_button(
                label="Download SVG Image",
                data=file,
                file_name="function_graph.svg",
                mime="image/svg+xml"
            )
    except FileNotFoundError:
        st.error("SVG file not found. Please check if it was created correctly.")
def graph2(x, function_input1, function_input2, name1, name2):

    # Create a symbolic function
    

    col7, col8 = st.columns(2)
    with col7:
        x_min = st.number_input(f"Enter the minimum value for {x}", value=0, step=1)
    with col8:
        x_max = st.number_input(f"Enter the maximum value for {x}", value=10, step=1)

    x_vals = np.linspace(x_min, x_max, 1000)
    y_vals1 = function_input1(x_vals)
    y_vals2 = function_input2(x_vals)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_vals, y=y_vals1, mode='lines', name=name1))
    fig.add_trace(go.Scatter(x=x_vals, y=y_vals2, mode='lines', name=name2))

    fig.update_layout(
        title=f"Graph of System of Ecuations",
        xaxis_title="x",
        yaxis_title=f"y",
        showlegend=True,
        margin=dict(l=0, r=0, t=40, b=0),
        hovermode="closest"
    )

    st.plotly_chart(fig)

    svg_file = "function_graph.svg"
    pio.write_image(fig, svg_file, format='svg', engine='kaleido')
    # Check if the SVG file was created
    try:
        with open(svg_file, "rb") as file:
            st.download_button(
                label="Download SVG Image",
                data=file,
                file_name="function_graph.svg",
                mime="image/svg+xml"
            )
            #skdsd
    except FileNotFoundError:
        st.error("SVG file not found. Please check if it was created correctly.")

def validar_numeros(entrada):
    try:
        # Convertir la entrada en una lista de números
        numeros = list(map(float, entrada.split()))
        return entrada
    except ValueError:
        # Si hay un error, la entrada no es válida
        return None


def graph_with_points(x_values, y_values, function, x_symbol = sp.symbols("x")):

    function = sp.lambdify(x_symbol, function, "numpy")

    x_min = min(x_values) - 1
    x_max = max(x_values) + 1
    x_vals = np.linspace(x_min, x_max, 500)
    y_vals = [function(x_val) for x_val in x_vals]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', name='Polynomial P(x)'))
    fig.add_trace(go.Scatter(x=x_values, y=y_values, mode='markers', name='Data Points'))


    fig.update_layout(
        title=f"Graph of the Interpolation",
        xaxis_title=str(x_symbol),
        yaxis_title=f"y",
        showlegend=True,
        margin=dict(l=0, r=0, t=40, b=0),
        hovermode="closest"
    )

    st.plotly_chart(fig)

    # Add value calculator
    st.subheader("Calculate Value at Point")
    x_calc = st.number_input(
        "Enter x value",
        value=float(sum(x_vals)/len(x_vals)),
        min_value=float(min(x_vals)),
        max_value=float(max(x_vals))
    )
    y_calc = float(function(x_calc))
    st.write(f"Q({x_calc}) = {y_calc}")

    svg_file = "function_graph.svg"
    pio.write_image(fig, svg_file, format='svg', engine='kaleido')

    
    # Check if the SVG file was created
    try:
        with open(svg_file, "rb") as file:
            st.download_button(
                label="Download SVG Image",
                data=file,
                file_name="function_graph.svg",
                mime="image/svg+xml"
            )
    except FileNotFoundError:
        st.error("SVG file not found. Please check if it was created correctly.")
