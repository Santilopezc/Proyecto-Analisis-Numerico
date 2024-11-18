import pandas as pd
import streamlit as st
import sympy as sp
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
    if not aprox and table is None:
        st.warning("El método no converge")
        return
    elif not aprox:
        st.warning("El método no converge") 
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