import numpy as np
from scipy.stats import norm 

def get_normal_standard_data(z_score: float) -> dict:
    x_points = np.linspace(-4, 4, 401)

    pdf_points = norm.pdf(x_points)
    cdf_points = norm.cdf(x_points)

    pdf_at_z = norm.pdf(z_score)
    cdf_at_z = norm.cdf(z_score)

    # 4. Ensamblar la respuesta JSON con la estructura exacta requerida
    response_data = {
        "metadata": {
            "formula": "Distribución Normal Estándar",
            "parameters": {
                "z_score": z_score
            }
        },
        "result": {
            # Redondeamos para que coincida con el ejemplo del prompt
            "pdf_at_z": round(pdf_at_z, 4),
            "cdf_at_z": round(cdf_at_z, 4)
        },
        "graph_data": {
            "title": "Función de Densidad y Distribución Normal Estándar",
            "datasets": [
                {
                    "label": "Densidad (PDF)",
                    "type": "line",
                    "x": x_points.tolist(), # Convertimos los arrays de numpy a listas
                    "y": pdf_points.tolist()
                },
                {
                    "label": "Acumulada (CDF)",
                    "type": "line",
                    "x": x_points.tolist(),
                    "y": cdf_points.tolist()
                }
            ],
            "marker": {
                "z": z_score,
                "pdf": round(pdf_at_z, 4),
                "cdf": round(cdf_at_z, 4)
            }
        }
    }
    return response_data

def get_normal_cdf_data(z_score: float) -> dict:
    cdf_value = norm.cdf(z_score)
    x_range = np.linspace(-4, 4, 401)
    y_range_pdf = norm.pdf(x_range)

    response_data = {
        "metadata": {"formula": "Función de Distribución Acumulada (CDF) - Normal Estándar", "parameters": {"z_score": z_score}},
        "result": {
            "cdf": cdf_value,
            "area_description": f"El {cdf_value:.2%} del área se encuentra a la izquierda de Z={z_score}"
        },
        "graph_data": {
            "title": f"Área Acumulada para Z = {z_score}", "x_label": "Z-score", "y_label": "Densidad",
            "x_range": x_range.tolist(), "y_range": y_range_pdf.tolist(), "shaded_area_limit": z_score
        }
    }
    return response_data