import array
from .utilities import dot

class Matrix:
    def __init__(self, rows, cols, fill=None):
        self.rows = rows
        self.cols = cols
        # case fill == None there is no input list
        if fill is None:
            self.data = array.array('d', [0] * (rows * cols))  # Initialization
        else:
            self.data = array.array('d', fill) 

    def __setitem__(self, indices, value):
        """Overload of [] for save the data"""
        if isinstance(indices, tuple) and len(indices) == 2:
            r, c = indices
            if isinstance(r, int) and isinstance(c, int):
                # simple case: A[i, j] = value
                self.data[r * self.cols + c] = value
            elif isinstance(r, int) and c == slice(None):
                # Case: A[i, :] = lista_valori
                if not isinstance(value, list) or len(value) != self.cols:
                    raise ValueError("Error, The dimension not concide")
                for j in range(self.cols):
                    self.data[r * self.cols + j] = value[j]
            elif r == slice(None) and isinstance(c, int):
                # Case: A[:, j] = lista_valori
                if not isinstance(value, list) or len(value) != self.rows:
                    raise ValueError("Error, The dimension not concide")
                for i in range(self.rows):
                    self.data[i * self.cols + c] = value[i]
            else:
                raise IndexError("Format not allowed")
        else:
            raise IndexError("Index not valid")

    def __getitem__(self, indices):
        """Overload of [] for access the data"""
        if isinstance(indices, tuple) and len(indices) == 2:
            r, c = indices
            if isinstance(r, int) and isinstance(c, int):
                # simple case: A[i, j]
                return self.data[r * self.cols + c]
            elif isinstance(r, int) and c == slice(None):
                # Case: A[i, :] → give the ith row
                return Matrix(1,self.cols,[self.data[r * self.cols + j] for j in range(self.cols)])
            elif r == slice(None) and isinstance(c, int):
                # Case: A[:, j] → give the jth column
                return Matrix(self.rows,1,[self.data[i * self.cols + c] for i in range(self.rows)])
            elif isinstance(r, slice) and isinstance(c, slice):
            # Case: A[i:i_max, j:j_max] → gives back a sub_matrix
                row_start, row_end = r.start or 0, r.stop or self.rows
                col_start, col_end = c.start or 0, c.stop or self.cols
                n_row = row_end-row_start +1
                n_col = col_end - col_start +1
                
                submatrix = [
                    self.data[i * self.cols + j]
                    for i in range(row_start, row_end+1)
                    for j in range(col_start, col_end+1)
                ]
                
            #the sub-matrix will be an object of my class matrix
                return Matrix(n_row,n_col,submatrix)
            else:
                raise IndexError("Indexes not allowed")
        else:
            raise IndexError("Indexes not allowed")
    def flatten(self):
        #The data structure is already a 1D array, just gives back the array
        return self.data
    def transpose(self):
        """Gives back the transpose of our Matrix"""
        transposed = Matrix(self.cols, self.rows)  # change rows with columns
        
        for r in range(self.rows):
            for c in range(self.cols):
                transposed[c, r] = self[r, c]  # switch of the indexes
        
        return transposed

    def __add__(self, other):
        if not isinstance(other, Matrix):
            raise TypeError("Type not allowed")

        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Dimension must concide")

        new_data = [self.data[i] + other.data[i] for i in range(len(self.data))]
        return Matrix(self.rows, self.cols, new_data)
    
    def __sub__(self, other):
        if not isinstance(other, Matrix):
            raise TypeError("Type not allowed")

        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Dimension must concide")

        new_data = [self.data[i] - other.data[i] for i in range(len(self.data))]
        return Matrix(self.rows, self.cols, new_data)

    def __repr__(self):
        """gives the matrix as a string"""

        return "\n".join(
            " ".join(f"{self.data[i * self.cols + j]:.2f}" for j in range(self.cols))
            for i in range(self.rows)
         )
    def __mul__(self,other):
        if isinstance(other,Vector):
            if self.cols != other.rows:
                raise IndexError("Dimension not compatible")
            else:
                result = Vector(self.cols)
                for i in range(self.rows):
                    data1 = self[i,:].data
                    v1 = Vector(self.cols,True,data1)
                    result[i] = dot(v1,other)
                return result
        elif isinstance(other,Matrix):
            if self.cols != other.rows:
                raise IndexError('Dimension not compatible')
            else:
                result = Matrix(self.rows,other.cols)
                for i in range(self.rows):
                    for j in range(other.cols):
                        data1 = self[i,:].data
                        data2 = other[:,j].data
                        v1 = Vector(self.cols,True,data1)
                        v2 = Vector(self.cols,False,data2)
                        result[i,j] = dot(v1,v2)
                return result
        else: 
            raise TypeError("Type not allowed")
    @classmethod
    def eye(cls, size):
        v = array.array('d', [0] * (size*size))
        for i in range(size):
            v[i * size + i] = 1
        return cls(size,size,v)
    def square(self):
        if self.rows == self.cols:
            return True
        else: 
            return False
    def copy(self):
        result = Matrix(self.rows,self.cols,self.data)
        return result    

class Vector(Matrix):
    def __init__(self, dim, row_vector=False,fill=None):
        """This is a specif case of the previus class, column vector default, row vector if flag = True"""
        if row_vector:
            super().__init__(1, dim, fill)  # row vector 1xn
        else:
            super().__init__(dim, 1, fill)  # column vector nx1

    def __repr__(self):
        """The vector will be stored as a string (just for plotted)"""
        if self.rows == 1:
            return "RowVector: " + " ".join(f"{self.data[i]:.2f}" for i in range(self.cols))
        else:
            return "ColumnVector:\n" + "\n".join(f"{self.data[i]:.2f}" for i in range(self.rows))
    def length(self):
        if self.rows > 1:
            return self.rows
        else:
            return self.cols
    def __eq__(self, other):
        """ Overload the = operator to allow for assignment from a matrix
            that has one dimension equal to 1 (e.g., a row or a column)
        """
        if isinstance(other, Matrix):
            if other.rows == 1:
                # If the matrix has 1 row, convert it to a row vector
                self.data = other.data  # Or extract the row data
                self.rows = 1
                self.cols = other.cols
            elif other.cols == 1:
                # If the matrix has 1 column, convert it to a column vector
                self.data = other.data  # Or extract the column data
                self.rows = other.rows
                self.cols = 1
            else:
                # If it's not a row or column, leave the matrix as is
                self.data = other.data
                self.rows = other.rows
                self.cols = other.cols
        else:
            raise ValueError("Cannot assign a non-matrix to a Vector.")
    def __setitem__(self, index, value):
        """Overload of [] for save the data"""
        if isinstance(index, int) and index < max(self.rows,self.cols):
            self.data[index] = value
        elif isinstance(index,slice):
            if length(value) != length(self.data):
                raise IndexError("The 2 vectors have different dimension")
            else:
                self.data = value
        else:
            raise IndexError("Index not valid")

    def __getitem__(self, index):
        """Overload of [] for access the data"""
        if isinstance(index, int) and index < max(self.rows,self.cols):
            return self.data[index]
        elif isinstance(index,slice):
            index0 = index.start or 0
            index1 = index.stop or length(self.data)
            dim = index1-index0 +1
            new_data = [self[i] for i in range(index0,index1)]
            if self.rows == 1:
                return Vector(dim,True,new_data)
            else:
                return Vector(dim,False,new_data)
        else:
            raise IndexError("Indexes not allowed")
    def transpose(self):
        """Gives back the transpose of our vector"""
        if self.cols ==1:
            transposed = Vector(self.rows,False,None)  # change rows with columns
            transposed.data = self.data #here is enough to switch rows with cols since the data structure is 1D array
            return transposed
        else:
            transposed = Vector(self.cols,True,None)  # change rows with columns
            transposed.data = self.data #here is enough to switch rows with cols since the data structure is 1D array
            return transposed
    
    def is_vector(self):
        """ This method is needed because the dot product works for general type
            that are scalar or vector
        """
        return True

    def __mul__(self,other):
        if isinstance(other,Matrix):
            if self.cols != other.rows:
                raise IndexError('Dimension not coincide')
            else:
                result = Vector(self.cols,True,None)
                for i in range(other.cols):
                    data1 = other[:,i].data
                    v1 = Vector(self.cols,True,data1)
                    result[i] = dot(v1,self)
                return result
        else: 
            raise TypeError("Type not allowed")