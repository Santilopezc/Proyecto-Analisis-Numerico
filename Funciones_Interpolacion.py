import numpy as np
from sympy import symbols, expand, simplify

x = symbols('x')

def construir_polinomio_newton(x_str, y_str, x_str): #Entrega el polinomio y la tabla de diferencias divididas
    
    x_vals = np.array(list(map(float, x_str.split())) )
    y_vals = np.array(list(map(float, y_str.split())) )
    n = len(x_vals)
    tabla = np.zeros((n, n+1))
    tabla[:, 0] = x_vals
    tabla[:, 1] = y_vals

    # Llenar la tabla de diferencias divididas
    for j in range(2, n+1):
        for i in range(j-1, n):
            tabla[i, j] = (tabla[i, j-1] - tabla[i-1, j-1]) / (tabla[i, 0] - tabla[i-j+1, 0])

    # Polinomio inicializado en el primer término
    polinomio = tabla[0, 1]  # Primer coeficiente de diferencias divididas (f[x0])

    # Producto acumulativo de términos (x - x_vals[i])
    producto_acumulado = 1
    for j in range(2, n+1):
        producto_acumulado *= (x - x_vals[j - 2])
        polinomio += tabla[j-1, j] * producto_acumulado

    # Expandir el polinomio para obtener su forma final
    polinomio_expandido = expand(polinomio)
    return polinomio_expandido, tabla

def polinomio_lagrange(x_str, y_str): #Entrega el polinomio
    x_vals = np.array(list(map(float, x_str.split())) )
    y_vals = np.array(list(map(float, y_str.split())) )

    n = len(x_vals)
    polinomio = 0

    for i in range(n):
        # Calcular el polinomio base de Lagrange L_i(x)
        L_i = 1
        for j in range(n):
            if i != j:
                L_i *= (x - x_vals[j]) / (x_vals[i] - x_vals[j])

        # Sumar f(x_i) * L_i(x) al polinomio total
        polinomio += y_vals[i] * L_i

    # Expandir y simplificar el polinomio para obtener la forma final
    polinomio_expandido = expand(simplify(polinomio))
    return polinomio_expandido





def spline_lineal(x_str, y_str, x_i_str):

    x_vals = np.array(list(map(float, x_str.split())) )
    y_vals = np.array(list(map(float, y_str.split())) )
    puntos = list(zip(x_vals, y_vals))
    x_float = float(x_i_str)

    # Ordenar puntos por su valor x para asegurarse de que están en orden
    puntos = sorted(puntos)

    # Recorrer cada intervalo y calcular el valor de spline lineal si x está en ese intervalo
    for i in range(len(puntos) - 1):
        x_i, y_i = puntos[i]
        x_next, y_next = puntos[i + 1]

        # Verificar si x está en el intervalo actual
        if x_i <= x_float <= x_next:
            # Calcular el valor del spline lineal en x
            m = (y_next - y_i) / (x_next - x_i)  # Pendiente
            return y_i + m * (x_float - x_i)

    # Si x está fuera de los límites de los puntos, devolver None o un mensaje
    return None
