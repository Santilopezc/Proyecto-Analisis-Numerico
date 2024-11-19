import numpy as np
import scipy as sp 
import pandas as pd
import streamlit as st


def make_tableMat(x_m_list,errores ):
    #x_m_list = np.transpose(x_m_list)
    #np.append(x_m_list,errores)
    table = pd.DataFrame(x_m_list[1:], columns = x_m_list[0])
    table["Error"] = errores
    return table

def calculate_error(X,X_L, error_rel):

    error = np.max(np.abs(X-X_L))
    if error_rel == 1:
        error = np.max(np.abs((X-X_L)/X))
    if error_rel == 2:
        error = np.max(np.abs((X-X_L)))/np.max(np.abs(X))
    return(error)

def rad_esp(T):
    eig = np.linalg.eigvals(T)
    rsp = np.max(np.abs(eig))
    return(rsp)

def Jacobi(A,b,X_i,tol,niter, error_rel = False):
   errores = [ 100]
  
   n = len(b.split())
   X_val = []
   X_num = []
   for i in range(n):
       X_num.append("X_"+ str(i+1))
   X_val.append(X_num)
   
   dim0 = len(A.split(";"))
   for i in range(len(A.split(";"))):
       dim1 = len(A.split(";")[i].split())
       if dim0 != dim1: 
        st.warning(f"La matrix añadida tiene dimensiones {dim0},{dim1} en la fila {i+1}; pero debe ser cuadrada")
        return("Nan",["Nan"],"Nan")
   
   Am = np.array([list(map(float, row.split())) for row in A.split(';')])

    
   bm = np.array(list(map(float, b.split())))
   
   if len(Am) != len(bm): 
       st.warning(f"La matrix añadida tiene dimensiones {len(Am)}x{len(Am)} y el vector b de constantes es {len(bm)}, pero deben ser iguales")
       return("Nan",["Nan"],"Nan")
   
   X = np.array(list(map(float, X_i.split())) )
   if len(Am) != len(X): 
    st.warning(f"La matrix añadida tiene dimensiones {len(Am)}x{len(Am)} y el vector de iniciales es {len(X)}, pero deben ser iguales")
    return("Nan",["Nan"],"Nan")
   D = np.diag(np.diagonal(Am))
   L = -1*np.tril(Am,-1)
   U = -1*np.triu(Am,1)
   X_val.append(X)
   
   T = np.linalg.inv(D)@(L+U)
   C = np.linalg.inv(D)@bm
   if rad_esp(T) >= 1:
       st.warning("La matriz ingresada no converge, pues su radio espectral es mayor o igual a 1")
       return("Nan",["Nan"],rad_esp(T))
 
   #print(T@X)
   E = (Am @ X) - bm
   
   if np.allclose(E, np.zeros(n), atol = tol) :
           return(make_tableMat(X_val,errores))
       
   for i in range( 1, niter):
       X_L = X
       X = T@X + C
       X_val.append(X)
       error = calculate_error(X,X_L,error_rel)
       errores.append(error)
       if error < tol:
           return(X,make_tableMat(X_val,errores),rad_esp(T))
   st.warning("El método no ha obtenido una solución con la cantidad de iteraciones máxima")
   return(X,make_tableMat(X_val,errores),rad_esp(T))
   #print(make_tableMat(X_val,errores).head(10))


def Gauss_Seidel(A,b,X_i,tol,niter, error_rel = False):
   errores = [ 100]
   n = len(b.split())
   X_val = []
   X_num = []
   for i in range(n):
       X_num.append("X_"+ str(i+1))
   X_val.append(X_num)
   dim0 = len(A.split(";"))
   for i in range(len(A.split(";"))):
       dim1 = len(A.split(";")[i].split())
       if dim0 != dim1: 
        st.warning(f"La matrix añadida tiene dimensiones {dim0},{dim1} en la fila {i+1}; pero debe ser cuadrada")
        return("Nan",["Nan"],"Nan")
   Am = np.array([list(map(float, row.split())) for row in A.split(';')])
   
   bm = np.array(list(map(float, b.split())) )
   if len(Am) != len(bm): 
       st.warning(f"La matrix añadida tiene dimensiones {len(Am)}x{len(Am)} y el vector b de constantes es {len(bm)}, pero deben ser iguales")
       return("Nan",["Nan"],"Nan")
   X = np.array(list(map(float, X_i.split())) )
   if len(Am) != len(X): 
    st.warning(f"La matrix añadida tiene dimensiones {len(Am)}x{len(Am)} y el vector de iniciales es {len(X)}, pero deben ser iguales")
    return("Nan",["Nan"],"Nan")
   D = np.diag(np.diagonal(Am))
   L = -1*np.tril(Am,-1)
   U = -1*np.triu(Am,1)
   X_val.append(X)
   
   T = np.linalg.inv(D-L)@(U)
   C = np.linalg.inv(D-L)@np.transpose(bm)
   #print(bm)
   #print(T@X)

   E = (Am @ X) - bm

   
   if np.allclose(E, np.zeros(n), atol = tol) :
           return(make_tableMat(X_val,errores))
   if rad_esp(T) >= 1:
       st.warning("La matriz ingresada no converge, pues su radio espectral es mayor o igual a 1")
       return("Nan",["Nan"],rad_esp(T))
   for i in range( 1, niter):
       X_L = X
       X = T@np.transpose(X) + C
       X_val.append(X)
       error = calculate_error(X,X_L,error_rel)
       errores.append(error)
       if error < tol:
           return(X,make_tableMat(X_val,errores),rad_esp(T))
   #print(make_tableMat(X_val,errores).head(10))
   st.warning("El método no ha obtenido una solución con la cantidad de iteraciones máxima")
   return(X,make_tableMat(X_val,errores),rad_esp(T))
def SOR(A,b,X_i,tol,niter,w, error_rel = False):
   errores = [ 100]
   n = len(b.split())
   X_val = []
   X_num = []
   for i in range(n):
       X_num.append("X_"+ str(i+1))
   X_val.append(X_num)
   
   dim0 = len(A.split(";"))
   for i in range(len(A.split(";"))):
       dim1 = len(A.split(";")[i].split())
       if dim0 != dim1: 
        st.warning(f"La matrix añadida tiene dimensiones {dim0},{dim1} en la fila {i+1}; pero debe ser cuadrada")
        return("Nan",["Nan"],"Nan")
   Am = np.array([list(map(float, row.split())) for row in A.split(';')])
   bm = np.array(list(map(float, b.split())) )
   if len(Am) != len(bm): 
       st.warning(f"La matrix añadida tiene dimensiones {len(Am)}x{len(Am)} y el vector b de constantes es {len(bm)}, pero deben ser iguales")
       return("Nan",["Nan"],"Nan")
   X = np.array(list(map(float, X_i.split())) )
   if len(Am) != len(X): 
    st.warning(f"La matrix añadida tiene dimensiones {len(Am)}x{len(Am)} y el vector de iniciales es {len(X)}, pero deben ser iguales")
    return("Nan",["Nan"],"Nan")
   D = np.diag(np.diagonal(Am))
   L = -1*np.tril(Am,-1)
   U = -1*np.triu(Am,1)
   X_val.append(X)
   T = np.linalg.inv(D-w*L)@((1-w)*D+w*U)
   C = w*np.linalg.inv(D-w*L)@np.transpose(bm)
   print(bm)
   #print(T@X)
   E = (Am @ X) - bm

   
   if np.allclose(E, np.zeros(n), atol = tol) :
           return(make_tableMat(X_val,errores))
   if rad_esp(T) >= 1:
       st.warning("La matriz ingresada no converge, pues su radio espectral es mayor o igual a 1")
       return("Nan",["Nan"],rad_esp(T))
   for i in range( 1, niter):
       X_L = X
       X = T@np.transpose(X) + C
       X_val.append(X)
       error = calculate_error(X,X_L,error_rel)
       errores.append(error)
       if error < tol:
           return(X,make_tableMat(X_val,errores), rad_esp(T))
   st.warning("El método no ha obtenido una solución con la cantidad de iteraciones máxima")
   return(X,make_tableMat(X_val,errores),rad_esp(T))
"""A = [[3,0,2],[2,6,2],[7,0,9]]
b = [10,10,10]
X_i = [1,2,-30]
print(SOR(A,b,X_i,0.0005,100,1.1))
print(Gauss_Seidel(A,b,X_i,0.0005,100, True))  """
    

