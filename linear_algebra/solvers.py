# solvers.py
from .matrix import Matrix,Vector 
from .utilities import norm
from math import sqrt

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
        raise TypeError('A must be a square matrix')
def Cholesky(A: Matrix):
    if  A.square():   
        H = Matrix(A.rows, A.cols)  # Initialization

        for i in range(A.rows):
            # diagonal element
            H[i, i] = sqrt(A[i, i] - sum(H[i, k]**2 for k in range(i)))

            for j in range(i + 1, A.rows):  # j > i for obatain the lower triangular matrix
                H[j, i] = (A[j, i] - sum(H[j, k] * H[i, k] for k in range(i))) / H[i, i]

        return H
    else:
        raise TypeError("A must be a square matrix")
def direct_solver(L:Matrix,U:Matrix,b:Vector):
    x = Vector(b.length(),False,None)
    y = Vector(b.length(),False,None)
    # Forward substitution (Ly = b)
    y[0] = b[0]/L[0,0]
    for i in range(1, L.rows):
        y[i] = (b[i] - sum(L[i, k] * y[k] for k in range(0, i)))/ L[i, i]

    # Backward substitution (Ux = y)
    x[-1] = y[-1] / U[-1, -1]
    for i in range(L.rows - 2, -1, -1):  
        x[i] = (y[i] - sum(U[i, k] * x[k] for k in range(i + 1, L.cols))) / U[i, i]
    
    return x,L,U

def solve(A: Matrix,b:Vector,Lower=None,Upper=None):
    if A.cols != b.length():
            raise IndexError("Dimension not compatible")
    else:
        if Lower is None and Upper is None :
            L,U = LU(A)
            return direct_solver(L,U,b)
        else:
            return direct_solver(Lower,Upper,b)

def Jacobi(A:Matrix, b: Vector):
    #Initialization of the method
    max_it = 1000
    eps = 1e-6
    err = 1+eps
    it = 0
    x = Vector(A.rows,False,None)
    x_old = x.copy()
    while(err > eps and it < max_it):
        for i in range(A.rows):
            x[i] = (1.0/A[i,i])* (b[i] - sum(A[i,j]*x_old[j] for j in range(A.cols) if j != i))
        # evaluation of the error
        diff = x-x_old
        x_old = x
        err = norm(diff,'L2')
        # update iteratio number
        it += 1
    if it< max_it:
        return x
    else:
        raise IndexError('Jacobi is diverged') 
    
