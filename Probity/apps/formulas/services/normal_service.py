import math
import numpy as np

def calculate_normal_pdf(z: float) -> float:
    """
    Calcula la Función de Densidad de Probabilidad (PDF) para un z-score
    Esta es la altura de la campana de Gauss en el punto z.
    """
    # Fórmula: (1 / sqrt(2*pi)) * e^(-z^2 / 2)
    pi = math.pi
    e = math.e
    return (1/ math.sqrt(2*pi)) * (e**(-0.5 * z**2))

def get_normal_standard_data(z_score: float) -> dict:
    """
    Prepara el diccionario completo con todos los datos para la API
    """
    #1. Calcular el resultado para el 'z_score' especifico
    pdf_at_z = calculate_normal_pdf(z_score)

    x_range = np.arange(-4.0, 4.1, 0.1).tolist()
    y_range = [calculate_normal_pdf(z) for z in x_range]

    response_data = {
        "metadata": {
            "formula": "Normal Estándar",
            "parameters": {"z_score": z_score}
        },
        "result": {
            "pdf_at_z": pdf_at_z
        },
        "graph_data": {
            "title": "Función de Densidad Normal Estándar",
            "x_label": "Z-score",
            "y_label": "Densidad",
            "x_range": x_range,
            "y_range": y_range,
            "marker": {
                "z": z_score,
                "pdf": pdf_at_z
            }
        }
    }
    return response_data
