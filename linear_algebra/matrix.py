import array

class Matrix:
    def __init__(self, rows, cols, fill=None):
        self.rows = rows
        self.cols = cols
        
        # case fill == None there is no input list
        if fill is None:
            self.data = [0] * (rows * cols)  # Initialization
        else:
            self.data = fill 

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
