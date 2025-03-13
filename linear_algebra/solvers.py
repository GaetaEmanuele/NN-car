# solvers.py
from .matrix import Matrix,Vector 

def LU(A: Matrix,b:Vector):
    if A.square():    
        L = Matrix.eye(A.rows)
        U = A.copy()
        n = A.rows
        for j in range(n):
            for i in range(j+1,n):
                L[i,j] = U[i,j]/U[j,j]
                for k in range(j,n):
                    U[i,k] -= L[i,j] * U[j,k]
        
        if A.cols != b.length():
            raise IndexError("Dimension not compatible")
        else:
            x = Vector(b.length(),False,None)
            y = Vector(b.length(),False,None)
            # Forward substitution (Ly = b)
            y[0] = b[0]
            for i in range(1, A.rows):
                y[i] = b[i] - sum(L[i, k] * y[k] for k in range(0, i))

            # Backward substitution (Ux = y)
            x[-1] = y[-1] / U[-1, -1]
            for i in range(A.rows - 2, -1, -1):  
                x[i] = (y[i] - sum(U[i, k] * x[k] for k in range(i + 1, A.cols))) / U[i, i]

            return x,L,U
    else:
        raise TypeError('A must be a square matrix')

def solve(A: Matrix,b):
    return LU(A,b)
