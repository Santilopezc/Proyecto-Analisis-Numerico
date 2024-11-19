import numpy as np
from sympy import symbols, expand, simplify
from scipy.interpolate import CubicSpline

x = symbols('x')

def polinomio_Vandermonde(x_str, y_str, x_eval): # Retorna polinomio y evaluación del mismo en x_val
    # Definir los puntos de datos conocidos
    x_points = np.array(list(map(float, x_str.split())) )
    y_points = np.array(list(map(float, y_str.split())) )
    puntos = zip(x_points, y_points)
    puntos = sorted(puntos)
    x_vals, y_vals = zip(*puntos)
    
    x_eval = float(x_eval)
    # Construir la matriz de Vandermonde
    A = np.vander(x_points, increasing=False)

    # Resolver el sistema de ecuaciones para encontrar los coeficientes
    coeffs = np.linalg.solve(A, y_points)

    n = len(coeffs)

    return sum(coeffs[i] * x**(n-1-i) for i in range(n)), sum(coeffs[i] * x_eval**(n-1-i) for i in range(n))

def construir_polinomio_newton(x_str, y_str): #Entrega el polinomio y la tabla de diferencias divididas
    
    x_vals = np.array(list(map(float, x_str.split())) )
    y_vals = np.array(list(map(float, y_str.split())) )
    x_vals, y_vals = zip(*sorted(zip(x_vals, y_vals)))
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
    x_vals, y_vals = zip(*sorted(zip(x_vals, y_vals)))

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



def spline_cubico(x_str, y_str): # Entrega el polinomio correspondiente a cada intervalo y las parejas deben estar en orden acendente

    x_vals = np.array(list(map(float, x_str.split())) )
    y_vals = np.array(list(map(float, y_str.split())) )
    x_vals, y_vals = zip(*sorted(zip(x_vals, y_vals)))
    # Calcular el spline cúbico
    cs = CubicSpline(x_vals, y_vals, bc_type='natural')

    # Crear una lista para almacenar los polinomios de cada intervalo
    polinomios_expandidos = []

    # Iterar sobre cada intervalo
    for i in range(len(x_vals) - 1):
        # Obtener los coeficientes del spline para el intervalo i
        coeffs = cs.c[:, i]  # Coeficientes para el intervalo i

        # Punto inicial del intervalo
        x_val = x_vals[i]

        # Construir el polinomio cúbico para el intervalo actual
        polynomial = 0
        for j in range(len(coeffs)):
            polynomial += coeffs[j] * (x - x_val)**(len(coeffs) - j - 1)

        # Expandir el polinomio
        expanded_polynomial = expand(polynomial)
        polinomios_expandidos.append(expanded_polynomial)

    return polinomios_expandidos

def spline_cuadratico(x_str, y_str): # Retorna lista de polinomios

    x_vals = np.array(list(map(float, x_str.split())) )
    y_vals = np.array(list(map(float, y_str.split())) )
    x_vals, y_vals = zip(*sorted(zip(x_vals, y_vals)))
    # Crear listas para almacenar los coeficientes y los polinomios de cada intervalo
    polinomios_expandidos = []
    n = len(x_vals) - 1  # Número de intervalos

    # Calcular las diferencias h_i entre los puntos
    h = [x_vals[i+1] - x_vals[i] for i in range(n)]

    # Resolver sistema para obtener los coeficientes c
    # Matriz tridiagonal para los valores de c_i
    A = np.zeros((n+1, n+1))
    b = np.zeros(n+1)

    # Rellenar la matriz y el vector b usando las condiciones de continuidad de la primera derivada
    for i in range(1, n):
        A[i, i-1] = h[i-1]
        A[i, i] = 2 * (h[i-1] + h[i])
        A[i, i+1] = h[i]
        b[i] = 3 * ((y_vals[i+1] - y_vals[i]) / h[i] - (y_vals[i] - y_vals[i-1]) / h[i-1])

    # Condiciones naturales (c_0 = 0 y c_n = 0)
    A[0, 0] = 1
    A[n, n] = 1

    # Resolver el sistema lineal para encontrar los valores de c
    c = np.linalg.solve(A, b)

    # Calcular los coeficientes a_i y b_i para cada intervalo y construir los polinomios
    for i in range(n):
        a_i = y_vals[i]
        b_i = (y_vals[i+1] - y_vals[i]) / h[i] - (h[i] * (2 * c[i] + c[i+1]) / 3)
        c_i = c[i]  # c_i ya fue calculado

        # Construir el polinomio cuadrático para el intervalo actual
        x_i = x_vals[i]
        polynomial = a_i + b_i * (x - x_i) + c_i * (x - x_i)**2

        # Expandir el polinomio
        expanded_polynomial = expand(polynomial)
        polinomios_expandidos.append(expanded_polynomial)

    return polinomios_expandidos

def spline_lineal(x_str, y_str, x_i_str):

    x_vals = np.array(list(map(float, x_str.split())) )
    y_vals = np.array(list(map(float, y_str.split())) )
    puntos = list(zip(x_vals, y_vals))
    x_vals, y_vals = zip(*sorted(puntos))
    x_float = float(x_i_str)

    # Ordenar puntos por su valor x para asegurarse de que están en orden
    puntos = sorted(puntos)
    eval = None
    polinomios = []
    # Recorrer cada intervalo y calcular el valor de spline lineal si x está en ese intervalo
    for i in range(len(puntos) - 1):
        x_i, y_i = puntos[i]
        x_next, y_next = puntos[i + 1]
        
        m = (y_next - y_i) / (x_next - x_i)
        polinomio = y_i + m * (x - x_i) 
        polinomios.append(polinomio)
        # Verificar si x está en el intervalo actual
        if x_i <= x_float <= x_next:
            # Calcular el valor del spline lineal en x
            m = (y_next - y_i) / (x_next - x_i)  # Pendiente
            eval = y_i + m * (x_float - x_i)

    # Si x está fuera de los límites de los puntos, devolver None o un mensaje
    if eval == None:
        eval = "Valor de x a evaluar por fuera de los límites"
    
    return polinomios, eval
