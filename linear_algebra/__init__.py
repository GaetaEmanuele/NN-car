# __init__.py

from .matrix import Matrix
from .solvers import *  # Importa tutto dal modulo solvers.py

__all__ = ["Matrix"] + [name for name in dir() if not name.startswith("_")]
