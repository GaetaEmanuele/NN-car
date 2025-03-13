# solvers.py
from .matrix import Matrix 

def LU(A: Matrix):
        L = Matrix.eye(A.rows)
        U = A.copy()
        n = A.rows
        for j in range(n):
            for i in range(j+1,n):
                L[i,j] = U[i,j]/U[j,j]
                for k in range(j,n):
                    U[i,k] -= L[i,j] * U[j,k]
        return L,U

def solve(A: Matrix,b):
    if A.square():
        if A.cols != len(b):
            raise IndexError("Dimension not compatible")
        else:
            L,U = LU(A)
            y,x = Vector(len(b),False,None)
            y[0] = b[0]
            for i in range(1,A.rows):
                for j in range(0,i):
                    y[i] = b[i] - sum(1/A[i,k] for k in range(0,j-1))
            x[-1] = y[-1]/U[-1,-1]
            for i in range(A.rows-2,0):
                for j in range(A.cols-1,i):
                    x[i] = y[i]/U[i,i] - sum(y[k]/A[i,k] for k in range(A.cols-1,j-1))
            return x
    else:
        raise TypeError('A must be a square matrix')
