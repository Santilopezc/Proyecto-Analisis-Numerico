import numpy as np
import scipy as sp 
import pandas as pd


def make_tableMat(x_m_list,errores ):
    #x_m_list = np.transpose(x_m_list)
    #np.append(x_m_list,errores)
    table = pd.DataFrame(x_m_list[1:], columns = x_m_list[0])
    table["Error"] = errores
    return table

def calculate_error(X,X_L, error_rel):

    error = np.max(np.abs(X-X_L))
    if error_rel:
        error = np.max(np.abs((X-X_L)/X))
    return(error)

def rad_esp(T):
    eig = np.linalg.eigvals(T)
    rsp = np.max(np.abs(eig))
    return(rsp)

def Jacobi(A,b,X_i,tol,niter, error_rel = False):
   errores = [ 100]
   n = len(A)
  
   X_val = []
   X_num = []
   for i in range(n):
       X_num.append("X_"+ str(i+1))
   X_val.append(X_num)
   X_val.append(X_i)
   Am = np.matrix(A)
   bm = np.array(b)
   X = np.array(X_i)
   D = np.diag(np.diagonal(Am))
   L = -1*np.tril(Am,-1)
   U = -1*np.triu(Am,1)
   
   T = np.linalg.inv(D)@(L+U)
   C = np.linalg.inv(D)@bm
   
   #print(T@X)
   E = (Am @ X) - b
   
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
   #print(make_tableMat(X_val,errores).head(10))


def Gauss_Seidel(A,b,X_i,tol,niter, error_rel = False):
   errores = [ 100]
   n = len(A)
  
   X_val = []
   X_num = []
   for i in range(n):
       X_num.append("X_"+ str(i+1))
   X_val.append(X_num)
   X_val.append(X_i)
   Am = np.matrix(A)
   
   bm = np.array(b)
   X = np.array(X_i)
   D = np.diag(np.diagonal(Am))
   L = -1*np.tril(Am,-1)
   U = -1*np.triu(Am,1)
   
   T = np.linalg.inv(D-L)@(U)
   C = np.linalg.inv(D-L)@np.transpose(bm)
   #print(bm)
   #print(T@X)
   E = (Am @ X) - b
   
   if np.allclose(E, np.zeros(n), atol = tol) :
           return(make_tableMat(X_val,errores))
       
   for i in range( 1, niter):
       X_L = X
       X = T@np.transpose(X) + C
       X_val.append(X)
       error = calculate_error(X,X_L,error_rel)
       errores.append(error)
       if error < tol:
           return(X,make_tableMat(X_val,errores),rad_esp(T))
   #print(make_tableMat(X_val,errores).head(10))
   
def SOR(A,b,X_i,tol,niter,w, error_rel = False):
   errores = [ 100]
   n = len(A)
  
   X_val = []
   X_num = []
   for i in range(n):
       X_num.append("X_"+ str(i+1))
   X_val.append(X_num)
   X_val.append(X_i)
   Am = np.matrix(A)
   
   bm = np.array(b)
   X = np.array(X_i)
   D = np.diag(np.diagonal(Am))
   L = -1*np.tril(Am,-1)
   U = -1*np.triu(Am,1)
   
   T = np.linalg.inv(D-w*L)@((1-w)*D+w*U)
   C = w*np.linalg.inv(D-w*L)@np.transpose(bm)
   print(bm)
   #print(T@X)
   E = (Am @ X) - b
   
   if np.allclose(E, np.zeros(n), atol = tol) :
           return(make_tableMat(X_val,errores))
       
   for i in range( 1, niter):
       X_L = X
       X = T@np.transpose(X) + C
       X_val.append(X)
       error = calculate_error(X,X_L,error_rel)
       errores.append(error)
       if error < tol:
           return(X,make_tableMat(X_val,errores), rad_esp(T))
"""A = [[3,0,2],[2,6,2],[7,0,9]]
b = [10,10,10]
X_i = [1,2,-30]
print(SOR(A,b,X_i,0.0005,100,1.1))
print(Gauss_Seidel(A,b,X_i,0.0005,100, True))  """
    
    
    
