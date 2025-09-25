import numpy as np

def calculate_bivariate_normal_pdf(x, y, mean_x, mean_y, std_dev_x, std_dev_y, correlation):
    """
    Calcula la PDF de la normal bivariada en un punto (x, y)
    según la fórmula de los apuntes.
    """
    if not (-1 < correlation < 1):
        raise ValueError("La correlación (ρ) debe estar entre -1 y 1.")
    if std_dev_x <= 0 or std_dev_y <= 0:
        raise ValueError("Las desviaciones estándar (σ) deben ser positivas.")

    # Normalizar x e y
    zx = (x - mean_x) / std_dev_x
    zy = (y - mean_y) / std_dev_y

    # Exponente de la fórmula
    exponent = - (zx**2 - 2 * correlation * zx * zy + zy**2) / (2 * (1 - correlation**2))

    # Coeficiente de la fórmula
    coeff = 1 / (2 * np.pi * std_dev_x * std_dev_y * np.sqrt(1 - correlation**2))

    return coeff * np.exp(exponent)

def get_bivariate_normal_data(mean_x, mean_y, std_dev_x, std_dev_y, correlation, x_value, y_value):
    """
    Prepara el diccionario completo para la API.
    """
    # 1. Calcular el resultado en el punto específico
    pdf_at_xy = calculate_bivariate_normal_pdf(x_value, y_value, mean_x, mean_y, std_dev_x, std_dev_y, correlation)

    # 2. Generar la malla de puntos para el gráfico 3D
    # Creamos un rango de -4 a 4 desviaciones estándar alrededor de cada media
    x_range = np.linspace(mean_x - 4 * std_dev_x, mean_x + 4 * std_dev_x, 50)
    y_range = np.linspace(mean_y - 4 * std_dev_y, mean_y + 4 * std_dev_y, 50)
    X, Y = np.meshgrid(x_range, y_range)

    # Calculamos el valor Z (altura) para cada punto de la malla
    Z = calculate_bivariate_normal_pdf(X, Y, mean_x, mean_y, std_dev_x, std_dev_y, correlation)

    # 3. Ensamblar la respuesta
    response_data = {
        "metadata": {
            "formula": "Distribución Normal Bivariada",
            "parameters": {
                "mean_x": mean_x, "mean_y": mean_y, "std_dev_x": std_dev_x,
                "std_dev_y": std_dev_y, "correlation": correlation,
                "x_value": x_value, "y_value": y_value
            }
        },
        "result": {
            "pdf_at_xy": pdf_at_xy
        },
        "graph_data": {
            "title": f"Superficie de Densidad (ρ={correlation})",
            "x_grid": x_range.tolist(),
            "y_grid": y_range.tolist(),
            "z_grid": Z.tolist() # La matriz de alturas
        }
    }
    return response_data