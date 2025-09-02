import math
import numpy as np
#ver tema de la simulacion

def calculate_normal_pdf(z: float) -> float:
    """
    Calcula la Función de Densidad de Probabilidad (PDF) para un z-score
    Esta es la altura de la campana de Gauss en el punto z.
    """
    # Fórmula: (1 / sqrt(2*pi)) * e^(-z^2 / 2)
    pi = math.pi
    e = math.e
    return (1/ math.sqrt(2*pi)) * (e**(-0.5 * z**2))

def calculate_normal_cdf(z: float) -> float:
    """
    Calcula la Función de Distribución Acumulada (CDF) para un z-score.
    """
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))

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


def get_normal_cdf_data(z_score: float) -> dict:
    cdf_value = calculate_normal_cdf(z_score) # Reutilizamos la función que ya teníamos

    x_range = np.arange(-4.0, 4.1, 0.1).tolist()
    y_range_pdf = [calculate_normal_pdf(z) for z in x_range]

    # 3. Ensamblar la respuesta JSON
    response_data = {
        "metadata": {
            "formula": "Función de Distribución Acumulada (CDF) - Normal Estándar",
            "parameters": {"z_score": z_score}
        },
        "result": {
            "cdf": cdf_value,
            "area_description": f"El {cdf_value:.2%} del área se encuentra a la izquierda de Z={z_score}"
        },
        "graph_data": {
            "title": f"Área Acumulada para Z = {z_score}",
            "x_label": "Z-score",
            "y_label": "Densidad",
            "x_range": x_range,
            "y_range": y_range_pdf,
            "shaded_area_limit": z_score
        }
    }
    return response_data
