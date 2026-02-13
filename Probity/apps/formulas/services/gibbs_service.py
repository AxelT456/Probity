import random
import string
import numpy as np
from sympy import *
from sympy.abc import x, y, u

def get_gibbs_data(limite_inferior: int, limite_superior: int, x0: int, y0: int, iteraciones: int, formula: str):
    """
    Prepara el diccionario completo, incluyendo datos para un scatter plot y un histograma 3D.
    """
    # 1. Llama a la función que hace la simulación para obtener los puntos (x, y)
    datos_calculados = calculate_gibbs_sampling(limite_inferior, limite_superior, x0, y0, iteraciones, formula)
    puntos_x = datos_calculados["x"]
    puntos_y = datos_calculados["y"]

    # --- INICIO DE LA NUEVA LÓGICA PARA EL HISTOGRAMA 3D ---

    # 2. Agrupar los puntos en una cuadrícula 2D para el histograma
    # Puedes ajustar el número de 'bins' para más o menos detalle
    bins = 20
    # H es la matriz de frecuencias, xedges/yedges son los bordes de los "cajones"
    H, xedges, yedges = np.histogram2d(puntos_x, puntos_y, bins=bins)

    # 3. Formatear los datos del histograma como [x_index, y_index, frecuencia]
    histogram_3d_data = []
    for i in range(len(xedges)-1):
        for j in range(len(yedges)-1):
            # Solo añadimos los puntos con frecuencia mayor a cero
            if H[i, j] > 0:
                histogram_3d_data.append([i, j, int(H[i, j])])

    # --- FIN DE LA NUEVA LÓGICA ---

    # 4. Ensamblar la nueva estructura de respuesta JSON
    response_data = {
        "metadata": {
            "formula": "Gibbs Sampling",
            "parameters": {
                "limite_inferior": limite_inferior, "limite_superior": limite_superior,
                "x0": x0, "y0": y0, "iteraciones": iteraciones, "formula": formula
            }
        },
        "result": {
            "total_points": len(puntos_x)
        },
        "graph_data": {
            "scatter_plot": {
                "title": "Gibbs Sampling: Trayectoria de (x, y)",
                "x": puntos_x,
                "y": puntos_y
            },
            "histogram_3d": {
                "title": "Densidad de Puntos del Muestreo de Gibbs",
                "data": histogram_3d_data,
                "x_bins": xedges.tolist(),
                "y_bins": yedges.tolist()
            }
        }
    }
    return response_data

def calculate_gibbs_sampling(limite_inferior: int, limite_superior: int, x_recibido: int, y_recibido: int, iteraciones: int, formula: str):
    """
    Realiza el muestreo de Gibbs. (Esta función no necesita cambios).
    """
    x, y, u = symbols('x y u')
    f = simplify(formula)
    f1 = integrate(f, (x, limite_inferior, limite_superior))
    f2 = integrate(f, (y, limite_inferior, limite_superior))
    fx_y = simplify(f/f1)
    fy_x = simplify(f/f2)
    Fx_y = integrate(fx_y, (x, limite_inferior, x))
    Fy_x = integrate(fy_x, (y, limite_inferior, y))
    ecuacion_u = Eq(u, Fx_y)
    ecuacion_v = Eq(u, Fy_x)
    f_x_i = solve(ecuacion_u, x)[1]
    f_y_i = solve(ecuacion_v, y)[1]
    
    puntos_x = [x_recibido]
    puntos_y = [y_recibido]
    
    for _ in range(iteraciones):
        x_i = f_x_i.subs({y: y_recibido, u: random.uniform(0, 1)})
        y_i = f_y_i.subs({x: x_i, u: random.uniform(0, 1)}) # Corregido para usar el nuevo x_i
        
        x_recibido = x_i
        y_recibido = y_i
        
        puntos_x.append(x_recibido)
        puntos_y.append(y_recibido)

    puntos_x_float = [float(punto) for punto in puntos_x]
    puntos_y_float = [float(punto) for punto in puntos_y]

    return {"x": puntos_x_float, "y": puntos_y_float}