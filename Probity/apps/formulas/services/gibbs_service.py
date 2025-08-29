from sympy import *
import random
from sympy.abc import x,y,u
import string
init_printing(use_latex="mathjax")

def get_gibbs_data(limite_inferior:int, limite_superior:int , x0:int, y0:int, iteraciones:int, formula:string):
    """
    Prepara el diccionario completo con todos los datos para la API.
    """
    datos_mandar=calculate_gibbs_sampling(limite_inferior, limite_superior , x0, y0, iteraciones, formula)
    #datos_mandar={"x": puntos_x, "y": puntos_y}
    response_data={
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
            "data": datos_mandar
        },
        "graph_data": {
            "title": "Gibbs Sampling: Trayectoria de (x, y)",
            "datasets": [
                {"label": "x values", "data": datos_mandar["x"]},
                {"label": "y values", "data": datos_mandar["y"]}
            ]
        }
    }
    return response_data
    
def calculate_gibbs_sampling(limite_inferior:int, limite_superior:int , x_recibido:int, y_recibido:int, iteraciones:int, formula:string):
    """
    Realiza el muestreo de Gibbs para una función de densidad conjunta dada.
    """
    #definir las variables
    x,y,u = symbols('x y u')
    #tranforma la string a una formula manejable por sympy
    f= simplify(formula)
    #marginal de x
    f1 = integrate(f, (x, limite_inferior, limite_superior))
    #marginal de y
    f2 = integrate(f, (y, limite_inferior, limite_superior))
    #simplificar funciones
    fx_y=simplify(f/f1);fy_x=simplify(f/f2)
    #generamos funciones de densidad acumulada
    Fx_y=integrate(fx_y,(x,limite_inferior,x))
    Fy_x=integrate(fy_x,(y,limite_inferior,y))  
    #igual respecto a u las funciones (u sera una variable aleatorioa uniforme entre 0 y 1)
    ecuacion_u=Eq(u,Fx_y)
    ecuacion_v=Eq(u,Fy_x)
    #despejar f(x|y_0) y f(y|x_0)
    #verificar si [1] siempre es el positivo
    f_x_i=solve(ecuacion_u,x)[1] #[1] es para tomar el valor positivo
    f_y_i=solve(ecuacion_v,y)[1] #[1] es para tomar el valor positivo
    #Puntos recibidos iniciando con x0 y y0
    puntos_x=[x_recibido]
    puntos_y=[y_recibido]
    #calculo de los puntos
    for z in range(iteraciones):
        #valores aleatorios para x y y
        r1=random.uniform(0, 1)
        r2=random.uniform(0, 1)
        #calculo de los nuevos puntos
        x_i=f_x_i.subs({y: y_recibido, u: r1})
        y_i=f_y_i.subs({x: x_recibido, u: r2})
        #reasignacion de puntos x_i y y_i
        x_recibido=x_i
        y_recibido=y_i
        #almacenamiento de los puntos
        puntos_x.append(x_recibido)
        puntos_y.append(y_recibido)
    return {"x": puntos_x, "y": puntos_y}
    
    
