class Variable:
    def __init__(self, value):
        self.value = value
        self.grad = 0.0
        self._backward = lambda: None  # Funzione per la backpropagation
        self.parents = []  # Variabili da cui dipende

    def backward(self):
        # Imposta il gradiente iniziale solo se è il nodo finale
        if self.grad == 0.0:
            self.grad = 1.0

        # Chiama la funzione di backpropagation associata a questa variabile
        self._backward()

        # Propaga il gradiente a tutte le variabili da cui dipende
        for parent in self.parents:
            parent.backward()

    def __add__(self, other):
        if isinstance(other, Variable):
            out = Variable(self.value + other.value)
        else:  # supporta somma con un numero
            out = Variable(self.value + other)

        def _backward():
            self.grad += out.grad
            if isinstance(other, Variable):
                other.grad += out.grad

        out._backward = _backward
        out.parents = [self] if not isinstance(other, Variable) else [self, other]
        return out

    def __sub__(self, other):
        if isinstance(other, Variable):
            out = Variable(self.value - other.value)
        else:  # supporta sottrazione con un numero
            out = Variable(self.value - other)

        def _backward():
            self.grad += out.grad
            if isinstance(other, Variable):
                other.grad -= out.grad

        out._backward = _backward
        out.parents = [self] if not isinstance(other, Variable) else [self, other]
        return out

    def __mul__(self, other):
        if isinstance(other, Variable):
            out = Variable(self.value * other.value)
        else:  # supporta moltiplicazione con un numero
            out = Variable(self.value * other)

        def _backward():
            self.grad += other.value * out.grad
            if isinstance(other, Variable):
                other.grad += self.value * out.grad

        out._backward = _backward
        out.parents = [self] if not isinstance(other, Variable) else [self, other]
        return out

    def __truediv__(self, other):
        if isinstance(other, Variable):
            out = Variable(self.value / other.value)
        else:  # supporta divisione con un numero
            out = Variable(self.value / other)

        def _backward():
            self.grad += (1.0 / other.value) * out.grad
            if isinstance(other, Variable):
                other.grad -= (self.value / (other.value ** 2)) * out.grad

        out._backward = _backward
        out.parents = [self] if not isinstance(other, Variable) else [self, other]
        return out

    def __pow__(self, exponent):
        out = Variable(self.value ** exponent)

        def _backward():
            self.grad += (exponent * self.value ** (exponent - 1)) * out.grad

        out._backward = _backward
        out.parents = [self]
        return out
# Funzione di loss: MSE (incremental loss)
def mse_loss(y_true, y_pred):
    diff = y_true - y_pred
    return (diff * diff) / Variable(len(y_true))  # Media dei quadrati degli errori

# Esempio di utilizzo con due variabili
x = Variable(3.0)  # Predizione
y_true = Variable(5.0)  # Valore vero

# Definizione della loss come differenza quadratica
loss = mse_loss(y_true, x)

# Inizializzare la backpropagation dalla loss
loss.backward()

# Stampare il gradiente rispetto a x
print(f'Loss: {loss.value}, Gradiente di x: {x.grad}')  # Output: (Loss value, Gradient of x)
