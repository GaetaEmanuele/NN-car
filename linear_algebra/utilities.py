
def dot(a, b):
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):  
        return a * b  # scalar product between 2 real number (just their product)

    if hasattr(a, "is_vector") and a.is_vector() and hasattr(b, "is_vector") and b.is_vector():
        return sum(x * y for x, y in zip(a.data, b.data))  # scalar product between 2 number

    raise TypeError("Type of input data not valid")
