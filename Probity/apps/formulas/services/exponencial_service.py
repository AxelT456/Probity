import random
import math

def run_exponencial_trial(n: int, l:int) -> dict:
    """
    Simula x ensayos de exponencial
    """
    puntos=[]
    for i in range(n):
        miu = random.uniform(0,1)
        x = -math.log(1 - miu) / l
        puntos.append(x)
    return {"sucesion":puntos}
    
    
def get_exponencial_data(n: int, l:int) -> dict:
    outcome = run_exponencial_trial(n,l)

    response_data = {
        "metadata": {
            "formula": "Exponencial",
            "parameters": {"n": n, "l":l}
        },
        "result": {
            "sucesion": outcome["sucesion"]
        },
        "graph_data": {
            "title": "Simulación de distribución exponencial",
            "data": outcome["sucesion"]
        }
    }
    return response_data
