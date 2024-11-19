import numpy as np
import pandas as pd
import streamlit as st
from scipy.misc import derivative
import math
from utils import calculate_error, make_table

def bisection(function, a, b, tol, n, use_sig_digits = False):
    # Add verification that f is continous in [a,b]
    # Add graph
    # Add chart
    # 0. Verify if f(a) * f(b) < 0
    if function(a) * function(b) >= 0:
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
    st.warning('El método no converge')
    return x_m, make_table(x_m_list, f_list, errors)

def regla_falsa(function, a, b, tol, n, use_sig_digits = False):
    if function(a) * function(b) >= 0:
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
    st.warning('El método no converge')
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
    st.warning('El método no converge')
    return x_m, make_table(x_m_list, f_list, errors)
            
def newton(function, df, x0, tol, n, use_sig_digits = False):
    errors = [100]
    x_m_list = []
    f_list = []
    x_m = x0
    for i in range(n):
        if df(x_m) == 0:
            st.warning(f'La derivada de la función en {x_m} es igual a 0')
            return None, None
        x_m = x_m - function(x_m)/df(x_m)
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
    st.warning('El método no converge')
    return x_m, make_table(x_m_list, f_list, errors)

def punto_fijo(function, g, x0, tol, n, use_sig_digits = False):
    errors = [100]
    x_m_list = []
    f_list = []
    x_m = x0
    for i in range(n):
        x_m = g(x_m)
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
    st.warning('El método no converge')
    return x_m, make_table(x_m_list, f_list, errors)

def raices_multiples(function, df,d2f, x0, tol, n, use_sig_digits = False):
    errors = [100]
    x_m_list = []
    f_list = []
    x_m = x0
    for i in range(n):
        if df(x_m) == 0:
            st.warning(f'La derivada de la función en {x_m} es igual a 0')
            return None, None
        x_m = x_m - (function(x_m) * df(x_m)) / (df(x_m)**2 - function(x_m) * d2f(x_m))
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
    st.warning('El método no converge')
    return x_m, make_table(x_m_list, f_list, errors)

