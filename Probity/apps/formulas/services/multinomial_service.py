# multinomial_service.py
from .utils import factorial
import math

def calculate_multinomial_pmf(n: int, outcomes: list[int], probabilities: list[float]) -> float:
    """
    Calcula la probabilidad de una combinación específica en un experimento multinomial.
    """
    # Coeficiente multinomial: n! / (x1! * x2! * ... * xk!)
    denominator_factorials = 1
    for x in outcomes:
        denominator_factorials *= factorial(x)

    multinomial_coefficient = factorial(n) / denominator_factorials

    # Parte de las probabilidades: p1^x1 * p2^x2 * ... * pk^xk
    prob_product = 1.0
    for i in range(len(outcomes)):
        prob_product *= probabilities[i] ** outcomes[i]

    return multinomial_coefficient * prob_product

def get_multinomial_data(n: int, outcomes: list[int], probabilities: list[float], labels: list[str]) -> dict:
    """
    Prepara el diccionario completo con todos los datos para la API.
    """
    probability = calculate_multinomial_pmf(n, outcomes, probabilities)

    expected_values = [n * p for p in probabilities]

    response_data = {
        "metadata": {
            "formula": "Multinomial",
            "parameters": {
                "n": n, "outcomes": outcomes, "probabilities": probabilities, "category_labels": labels
            }
        },
        "result": {
            "probability": probability,
            "expected_values": expected_values
        },
        "graph_data": {
            "title": "Distribución Multinomial: Observado vs. Esperado",
            "x_label": "Categorías", "y_label": "Frecuencia",
            "labels": labels,
            "datasets": [
                {"label": "Frecuencia Observada", "data": outcomes},
                {"label": "Frecuencia Esperada", "data": expected_values}
            ]
        }
    }
    return response_data