from matrix import Matrix,Vector

def dot(a: Vector,b: Vector):
    dim1 = a.length()
    dim2 = b.length()
    sum = 0.0
    if dim1 != dim2:
        TypeError('The 2 vector have different dimension')
    else:
        sum += a[i]*b[i] for i in range(dim1)
        return sum
