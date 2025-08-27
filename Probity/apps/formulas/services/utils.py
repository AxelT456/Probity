#utils.py
import math

def factorial(n):
    """Calcula el factorial de un número"""
    if n<0:
        raise ValueError("El número debe ser no negativo")
    return math.factorial(n)

def combinations(n,k):
    """Calcula las combinaciones 'n en k'"""
    if k<0 or k>n:
        return 0
    return factorial(n)//(factorial(k)*factorial(n-k))

