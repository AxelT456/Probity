import math
import random
import numpy as np

def run_exponencial_simulation(n: int, rate: float) -> list[float]:
    """
    Simula 'n' variables aleatorias de una distribución exponencial.
    Usa el método de la transformada inversa.
    """
    if rate <= 0:
        raise ValueError("La tasa (lambda) debe ser positiva.")
    
    points = []
    for _ in range(n):
        # Genera un número aleatorio uniforme entre 0 y 1
        u = random.uniform(0, 1)
        # Aplica la función inversa de la CDF: -ln(1-u) / lambda
        x = -math.log(1 - u) / rate
        points.append(x)
    return points

def get_exponencial_data(n: int, rate: float) -> dict:
    simulation_points = run_exponencial_simulation(n, rate)

    max_val = max(simulation_points) if simulation_points else 5 / rate
    x_points = np.linspace(0, max_val, 401).tolist()
    
    # PDF teórica: f(x) = λ * e^(-λx)
    pdf_points = [rate * math.exp(-rate * x) for x in x_points]
    # CDF teórica: F(x) = 1 - e^(-λx)
    cdf_points = [1 - math.exp(-rate * x) for x in x_points]

    # 3. Ensamblar la respuesta JSON
    response_data = {
        "metadata": {
            "formula": "Distribución Exponencial",
            "parameters": {"n_simulaciones": n, "lambda": rate}
        },
        "result": {
            "simulation_points": simulation_points,
            "mean_of_simulation": sum(simulation_points) / len(simulation_points),
            "theoretical_mean": 1 / rate
        },
        "graph_data": {
            "title": f"Distribución Exponencial (λ={rate})",
            "simulation_data": simulation_points, # Para el histograma
            "theoretical_curves": [
                {
                    "label": "PDF Teórica", "type": "line",
                    "x": x_points, "y": pdf_points
                },
                {
                    "label": "CDF Teórica", "type": "line",
                    "x": x_points, "y": cdf_points
                }
            ]
        }
    }
    return response_data