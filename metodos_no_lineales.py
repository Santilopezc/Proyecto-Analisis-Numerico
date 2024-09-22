import numpy as np
import pandas as pd
import streamlit as st




def bisection(function, a, b, tol, n, use_sig_digits = False):
    # Add verification that f is continous in [a,b]
    # Add graph
    # Add chart
    # 0. Verify if f(a) * f(b) < 0
    if function(a) * function(b) > 0:
        st.warning(f'El intervalo [{a},{b}] es inadecuado')
        return None, None
    errors = [100]
    x_m_list = []
    f_list = []
    for i in range(n):
        # 1. Calculate x_m = b+a/2
        x_m = (b+a)/2
        x_m_list.append(x_m)
        f_x_m = function(x_m)
        f_list.append(f_x_m)
        
        if f_x_m == 0:
            return x_m, make_table(x_m_list, f_list, errors)
        # 2. Verify if f(X_m) is positive or negative
        # 3. Replace X_m with a or b, depending on the result of step 2
        if function(a) * f_x_m < 0:
            b = x_m
        else:
            a = x_m
        if i > 0:
            error = calculate_error(use_sig_digits, x_m, x_m_list, i)
            errors.append(error)
            # Stop when error is less than tolerance
            if error < tol:
                return x_m, make_table(x_m_list, f_list, errors)
    pass

def calculate_error(use_sig_digits: bool, x_m: float, x_list: list, index: int):
    if use_sig_digits:
        error = abs((x_m - x_list[index-1]) / x_m)
    else:
        error = abs(x_m - x_list[index-1])
    return error
    

def regla_falsa(function, a, b, tol, n, use_sig_digits = False):
    if function(a) * function(b) > 0:
        st.warning(f'El intervalo [{a},{b}] es inadecuado')
        return None, None
    errors = [100]
    x_m_list = []
    f_list = []
    for i in range(n):
        x_m = b - function(b) * ((b-a) / (function(b) - function(a)))
        x_m_list.append(x_m)
        f_x_m = function(x_m)
        f_list.append(f_x_m)
        if f_x_m == 0:
            return x_m, make_table(x_m_list, f_list, errors)
        if function(a) * f_x_m < 0:
            b = x_m
        else:
            a = x_m
        if i > 0:
            error = calculate_error(use_sig_digits, x_m, x_m_list, i)
            errors.append(error)
            if error < tol:
                return x_m, make_table(x_m_list, f_list, errors)




def secante(function, x0, x1, tol, n, use_sig_digits = False):
    errors = [100]
    x_m_list = []
    f_list = []
    x_m_prev = x0
    x_m = x1
    for i in range(n):
        x_m_new = x_m - (function(x_m) * (x_m - x_m_prev)) / (function(x_m) - function(x_m_prev))
        x_m_prev = x_m
        x_m = x_m_new
        x_m_list.append(x_m)
        f_x_m = function(x_m)
        f_list.append(f_x_m)
        if f_x_m == 0:
            return x_m, make_table(x_m_list, f_list, errors)
        if i > 0:
            error = calculate_error(use_sig_digits, x_m, x_m_list, i)
            errors.append(error)
            if error < tol:
                return x_m, make_table(x_m_list, f_list, errors)
            
def newton():
    pass
def punto_fijo():
    pass

def make_table(x_m_list, f_list, errors):
    table = pd.DataFrame({
        'X_m': x_m_list,
        'f(X_m)': f_list,
        'Error': errors
    })
    return table

def trial_function(x):
    return np.exp(-x) + x**2 -13