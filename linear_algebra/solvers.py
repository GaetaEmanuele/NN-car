# solvers.py
from .matrix import Matrix  

def LU(A: Matrix):
    if A.square():
        L = Matrix.eye(A.rows)
        U = A.copy()
        n = A.rows
        for j in range(n):
            for i in range(j+1,n):
                L[i,j] = U[i,j]/U[j,j]
                for k in range(j,n):
                    U[i,k] -= L[i,j] * U[j,k]
        return L,U
    else:
        raise TypeError("A is not a square Matrix")
    
