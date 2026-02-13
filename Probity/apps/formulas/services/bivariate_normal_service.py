import numpy as np

def calculate_bivariate_normal_pdf(x, y, mean_x, mean_y, std_dev_x, std_dev_y, correlation):
    # ... (esta función no necesita cambios) ...
    if not (-1 < correlation < 1):
        raise ValueError("La correlación (ρ) debe estar entre -1 y 1.")
    if std_dev_x <= 0 or std_dev_y <= 0:
        raise ValueError("Las desviaciones estándar (σ) deben ser positivas.")
    zx = (x - mean_x) / std_dev_x
    zy = (y - mean_y) / std_dev_y
    exponent = - (zx**2 - 2 * correlation * zx * zy + zy**2) / (2 * (1 - correlation**2))
    coeff = 1 / (2 * np.pi * std_dev_x * std_dev_y * np.sqrt(1 - correlation**2))
    return coeff * np.exp(exponent)

def get_bivariate_normal_data(mean_x, mean_y, std_dev_x, std_dev_y, correlation, x_value, y_value, n_simulations):
    """
    Prepara el diccionario con datos para el gráfico 3D Y el gráfico de dispersión 2D.
    """
    # --- Lógica existente para el gráfico 3D (sin cambios) ---
    pdf_at_xy = calculate_bivariate_normal_pdf(x_value, y_value, mean_x, mean_y, std_dev_x, std_dev_y, correlation)
    x_range = np.linspace(mean_x - 4 * std_dev_x, mean_x + 4 * std_dev_x, 50)
    y_range = np.linspace(mean_y - 4 * std_dev_y, mean_y + 4 * std_dev_y, 50)
    X, Y = np.meshgrid(x_range, y_range)
    Z = calculate_bivariate_normal_pdf(X, Y, mean_x, mean_y, std_dev_x, std_dev_y, correlation)

    # --- INICIO DE LA NUEVA LÓGICA PARA EL GRÁFICO 2D ---

    # 1. Construir la matriz de covarianza
    cov_xy = correlation * std_dev_x * std_dev_y
    cov_matrix = [[std_dev_x**2, cov_xy], [cov_xy, std_dev_y**2]]

    # 2. Generar 'n_simulations' puntos aleatorios
    points = np.random.multivariate_normal([mean_x, mean_y], cov_matrix, size=n_simulations)

    # 3. Separar los puntos en listas de coordenadas x e y
    scatter_x = points[:, 0].tolist()
    scatter_y = points[:, 1].tolist()

    # --- FIN DE LA NUEVA LÓGICA ---

    # 4. Ensamblar la respuesta JSON ahora con ambos tipos de datos
    response_data = {
        "metadata": {
            "formula": "Distribución Normal Bivariada",
            "parameters": {
                "mean_x": mean_x, "mean_y": mean_y, "std_dev_x": std_dev_x,
                "std_dev_y": std_dev_y, "correlation": correlation,
                "x_value": x_value, "y_value": y_value, "n_simulations": n_simulations
            }
        },
        "result": { "pdf_at_xy": pdf_at_xy },
        "graph_data": {
            "surface_3d": {
                "title": f"Superficie de Densidad (ρ={correlation})",
                "x_grid": x_range.tolist(),
                "y_grid": y_range.tolist(),
                "z_grid": Z.tolist()
            },
            "scatter_2d": {
                "title": f"Nube de Puntos de la Simulación ({n_simulations} puntos)",
                "x": scatter_x,
                "y": scatter_y
            }
        }
    }
    return response_data