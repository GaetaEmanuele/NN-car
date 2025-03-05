from linear_algebra import Matrix , Vector
#Example1 Matrix

A = Matrix(2, 3, [1.2345, 2.6789, 3.4567, 4.9999, 5.1234, 6.9876])

print('Example 1: ')
print()
print()
print(A)

c = A[0:1,0:1]
print()
print()
print(c)
print()
print()
b = A[:,1]
print(b)
print()
print()
d = A[0,:]
print(d)
print()
print('Example 2: ')

B = Matrix(2, 3, [1, 2, 3, 4, 5, 6])
C = Matrix(2,3,[0, 1, 2, 3, 4, 5])
A1 = B - C
A2 = B + C
print('sottrazione:')
print()
print(A1)
print()
print('somma: ')
print()
print(A2)
print()
print('Example3')
print()
print(C)
C = C.transpose()
print()
print(C)
print()
print('Example4')
v = Vector([1,2,3,4])
print(v)