import random

def run_bernoulli_trial(p: float, n:int) -> dict:
    """
    Simula x ensayos de Bernoulli
    Devuelve 1 (éxito) con probabilidad 'p', y 0(fracaso) con probabilidad '1-p'
    """
    if not (0<= p <=1):
        raise ValueError("La probabilidad 'p' debe estar entre 0 y 1")
    if not (0<n):
        raise ValueError("El numero de repeticiones debe de ser mayor a 0")
    sucesion=[]
    exts=0
    frcss=0
    #Repetir el experimento n veces
    for x in range(n):
        if random.uniform(0, 1)<p:
            sucesion.append("E")
            exts+=1
        else:
            sucesion.append("F")   
            frcss+=1
    #mandar la sucesion de Exitos y Fracasos, cantidades de E, cantidades de F
    return {"Sucesion":sucesion,"Exitos":exts,"Fracasos":frcss}
    
    
def get_bernoulli_data(p: float, n:int) -> dict:
    outcome = run_bernoulli_trial(p,n)
    
    prob_fracaso = 1 - p
    prob_exito = p

    response_data = {
        "metadata": {
            "formula": "Ensayo de Bernoulli",
            "parameters": {"p": p}
        },
        "result": {
            "data": outcome
        },
        "graph_data": {
            "title": f"Distribución Teórica de Bernoulli (p={p})",
            "categories": ["Éxitos", "Fracasos"], 
            "dataset": [outcome["Exitos"], outcome["Fracasos"]], 
            "probabilities": {
                "Exito":prob_exito, "Fracaso":prob_fracaso
            }
        }
    }
    return response_data
