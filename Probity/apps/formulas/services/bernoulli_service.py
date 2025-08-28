import random

def run_bernoulli_trial(p: float) -> int:
    """
    Simula un único ensayo de Bernoulli
    Devuelve 1 (éxito) con probabilidad 'p', y 0(fracaso) con probabilidad '1-p'
    """
    if not (0<= p <=1):
        raise ValueError("La probabilidad 'p' debe estar entre 0 y 1")
    
    if random.random()<p:
        return 1
    else:
        return 0
    
def get_bernoulli_data(p: float) -> dict:
    outcome = run_bernoulli_trial(p)

    prob_fracaso = 1 - p
    prob_exito = p

    response_data = {
        "metadata": {
            "formula": "Ensayo de Bernoulli",
            "parameters": {"p": p}
        },
        "result": {
            "simulation_outcome": outcome,
            "outcome_label": "Éxito" if outcome == 1 else "Fracaso"
        },
        "graph_data": {
            "title": f"Distribución Teórica de Bernoulli (p={p})",
            "x_label": "Resultado",
            "y_label": "Probabilidad",
            "labels": ["Fracaso (0)", "Éxito (1)"],
            "probabilities": [prob_fracaso, prob_exito]
        }
    }
    return response_data
