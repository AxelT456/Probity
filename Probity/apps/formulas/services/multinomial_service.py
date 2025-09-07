# multinomial_service.py
from .utils import factorial
import random

#ver tema de la simulacion
def calculate_multinomial_pmf(n: int, k: int, probabilities: list[float]) -> dict:
    """
    Simula n experimentos de k repeticiones cada uno con probabilidades dadas.
    Devuelve una lista de diccionarios con la frecuencia de cada resultado.
    """
    cumulative = []
    total = 0
    for p in probabilities:
        cumulative.append(total + p)
        total += p
    sucesion = []
    for i in range(n):  # ciclo general de número de experimentos
        rangos = {str(j+1): 0 for j in range(len(cumulative))}  # inicializar conteos

        for y in range(k):  # ciclo interno de repeticiones del experimento
            for z in range(len(cumulative)):
                if random.uniform(0, 1) < cumulative[z]:
                    rangos[str(z+1)] += 1
                    break
        sucesion.append(rangos.copy())
    return {"vectores":sucesion}

def analyze_vector_frequencies(simulation_results):
    vectors = []
    for sim in simulation_results:
        vectors.append(tuple(sim.values()))
    
    # Contar frecuencias
    from collections import Counter
    vector_counts = Counter(vectors)
    
    # Crear matriz para heatmap
    unique_vectors = list(vector_counts.keys())
    heatmap_matrix = []
    # Dynamically use all keys present in sim, sorted for consistency
    if simulation_results:
        keys = sorted(simulation_results[0].keys(), key=lambda x: int(x))
    else:
        keys = []
    for vector in unique_vectors:
        row = [1 if tuple(sim[k] for k in keys) == vector else 0 
               for sim in simulation_results]
        heatmap_matrix.append(row)
    
    return vector_counts, heatmap_matrix

def get_multinomial_data(n: int, k: int, probabilities: list[float]) -> dict:
    """
    Prepara el diccionario completo con todos los datos para la API.
    n:numero de experimentos, k: numero de veces por experimento
    probabilities: probabilidades dadas (son hasta n)
    """
    vectores = calculate_multinomial_pmf(n, k, probabilities)
    cosas = analyze_vector_frequencies(vectores["vectores"])
    # Convert tuple keys to strings for JSON serialization
    vector_counts_str = {str(k): v for k, v in cosas[0].items()}
    response_data = {
        "metadata": {
            "formula": "Multinomial",
            "parameters": {
                "n": n, "k": k, "probabilities": probabilities, "category_labels": 0
            }
        },
        "result": {
            "probability": 0,
            "sucesion": vectores,
            "vector_counts": vector_counts_str
        },
        "graph_data": {
            "title": "Distribución Multinomial: Observado vs. Esperado",
            "x_label": "Categorías", "y_label": "Frecuencia",
            "labels": 0,
            "datasets": [
                {"label": "Frecuencia Observada", "data": k},
                {"label": "Frecuencia Esperada", "data": 0}
            ],
            "title2":"Grafico de calor",
            "dataset":cosas[1]
        }
    }
    return response_data