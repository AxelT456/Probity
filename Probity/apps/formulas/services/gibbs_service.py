from sympy import *
import random
from sympy.abc import x,y,u
import string

def get_gibbs_data(limite_inferior:int, limite_superior:int , x0:int, y0:int, iteraciones:int, formula:string):
    """
    Prepara el diccionario completo con todos los datos para la API.
    """
    # Llama a la función que hace el cálculo principal
    datos_calculados = calculate_gibbs_sampling(limite_inferior, limite_superior, x0, y0, iteraciones, formula)
    
    # Ensambla la estructura de respuesta JSON
    response_data = {
        "metadata": {
            "formula": "Gibbs Sampling",
            "parameters": {
                "limite_inferior": limite_inferior,
                "limite_superior": limite_superior,
                "x0": x0,
                "y0": y0,
                "iteraciones": iteraciones,
                "formula": formula
            }  
        },
        "result": {
            "data": datos_calculados
        },
        "graph_data": {
            "title": "Gibbs Sampling: Trayectoria de (x, y)",
            "datasets": [
                {"label": "x values", "data": datos_calculados["x"]},
                {"label": "y values", "data": datos_calculados["y"]}
            ]
        }
    }
    return response_data
    
def calculate_gibbs_sampling(limite_inferior:int, limite_superior:int , x_recibido:int, y_recibido:int, iteraciones:int, formula:string):
    """
    Realiza el muestreo de Gibbs para una función de densidad conjunta dada.
    """
    # Definir las variables simbólicas
    x, y, u = symbols('x y u')
    
    # Tranforma el string a una formula manejable por sympy
    f = simplify(formula)
    
    # Calcular marginales e integrales simbólicamente
    f1 = integrate(f, (x, limite_inferior, limite_superior))
    f2 = integrate(f, (y, limite_inferior, limite_superior))
    
    fx_y = simplify(f/f1)
    fy_x = simplify(f/f2)
    
    Fx_y = integrate(fx_y, (x, limite_inferior, x))
    Fy_x = integrate(fy_x, (y, limite_inferior, y))  
    
    ecuacion_u = Eq(u, Fx_y)
    ecuacion_v = Eq(u, Fy_x)
    
    # Despejar para obtener las funciones inversas
    f_x_i = solve(ecuacion_u, x)[1]
    f_y_i = solve(ecuacion_v, y)[1]
    
    # Inicializar las listas de puntos
    puntos_x = [x_recibido]
    puntos_y = [y_recibido]
    
    # Bucle principal de la simulación
    for _ in range(iteraciones):
        r1 = random.uniform(0, 1)
        r2 = random.uniform(0, 1)
        
        # Calcular los nuevos puntos (aún son objetos de Sympy)
        x_i = f_x_i.subs({y: y_recibido, u: r1})
        y_i = f_y_i.subs({x: x_recibido, u: r2})
        
        x_recibido = x_i
        y_recibido = y_i
        
        puntos_x.append(x_recibido)
        puntos_y.append(y_recibido)

    puntos_x_float = [float(punto) for punto in puntos_x]
    puntos_y_float = [float(punto) for punto in puntos_y]

    # Devuelve las listas convertidas, que ahora son compatibles con JSON
    return {"x": puntos_x_float, "y": puntos_y_float}