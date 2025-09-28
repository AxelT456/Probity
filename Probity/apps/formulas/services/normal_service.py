import numpy as np
from scipy.stats import norm

def get_normal_distribution_data(mean: float, std_dev: float, x_value: float) -> dict:
    """
    Prepara el diccionario para una Distribución Normal General (no solo estándar).
    """
    # 1. Calcular los puntos para las curvas. El rango ahora es dinámico
    # para centrarse alrededor de la media.
    # Graficamos desde 4 desviaciones estándar a la izquierda hasta 4 a la derecha.
    x_min = mean - (4 * std_dev)
    x_max = mean + (4 * std_dev)
    x_points = np.linspace(x_min, x_max, 401)

    # 2. Calcular los valores de Y, pasando la media (loc) y la desviación (scale)
    pdf_points = norm.pdf(x_points, loc=mean, scale=std_dev)
    cdf_points = norm.cdf(x_points, loc=mean, scale=std_dev)

    # 3. Calcular los valores específicos para el x_value del usuario
    pdf_at_x = norm.pdf(x_value, loc=mean, scale=std_dev)
    cdf_at_x = norm.cdf(x_value, loc=mean, scale=std_dev)

    # 4. Ensamblar la respuesta JSON
    response_data = {
        "metadata": {
            "formula": "Distribución Normal",
            "parameters": {
                "mean": mean,
                "std_dev": std_dev,
                "x_value": x_value
            }
        },
        "result": {
            "pdf_at_x": round(pdf_at_x, 4),
            "cdf_at_x": round(cdf_at_x, 4)
        },
        "graph_data": {
            "title": f"Distribución Normal (μ={mean}, σ={std_dev})",
            "datasets": [
                {
                    "label": "Densidad (PDF)", "type": "line",
                    "x": x_points.tolist(), "y": pdf_points.tolist()
                },
                {
                    "label": "Acumulada (CDF)", "type": "line",
                    "x": x_points.tolist(), "y": cdf_points.tolist()
                }
            ],
            "marker": {
                "x": x_value,
                "pdf": round(pdf_at_x, 4),
                "cdf": round(cdf_at_x, 4)
            }
        }
    }
    return response_data