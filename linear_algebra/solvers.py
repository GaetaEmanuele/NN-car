# solvers.py
from .matrix import Matrix,Vector 
from math import sqrt

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
def Cholesky(A: Matrix, b: Vector):
    if A.square():
        H = Matrix(A.rows, A.cols, None)
    
        # 1st element of the diagonal
        H[0, 0] = sqrt(A[0, 0])
    
        for i in range(A.rows):
            # Diagonal element
            H[i, i] = sqrt(A[i, i] - sum(H[i, k]**2 for k in range(0, i)))
        
            # element below the diagonal
            for j in range(0, i):
                H[i, j] = (A[i, j] - sum(H[i, k] * H[j, k] for k in range(0, j))) / H[j, j]

        return H
    else:
        raise TypeError("A must be a square matrix")

def solve(A: Matrix,b):
    return LU(A,b)
