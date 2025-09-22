import random
from collections import Counter

def run_multinomial_simulation(num_experiments: int, num_trials: int, probabilities: list[float]) -> list[tuple]:
    """
    Simula n experimentos de k ensayos cada uno. Devuelve una lista de vectores de resultado.
    (Esta función no necesita cambios)
    """
    cumulative_probs = []
    total = 0
    for p in probabilities:
        total += p
        cumulative_probs.append(total)

    all_outcome_vectors = []
    num_categories = len(probabilities)

    for _ in range(num_experiments):
        outcome_counts = [0] * num_categories
        for _ in range(num_trials):
            rand_num = random.uniform(0, 1)
            for i, cum_prob in enumerate(cumulative_probs):
                if rand_num < cum_prob:
                    outcome_counts[i] += 1
                    break
        all_outcome_vectors.append(tuple(outcome_counts))
        
    return all_outcome_vectors

def get_multinomial_data(num_experiments: int, num_trials: int, probabilities: list[float], labels: list[str]) -> dict:
    """
    Prepara el diccionario completo con los datos formateados para un
    GRÁFICO DE BARRAS HORIZONTAL, según el componente ResultsChart.vue.
    """
    # 1. Ejecutar la simulación
    simulation_results = run_multinomial_simulation(num_experiments, num_trials, probabilities)
    vector_counts = Counter(simulation_results)
    most_common_vectors = vector_counts.most_common(20)
    most_frequent = most_common_vectors[0] if most_common_vectors else ((), 0)

    # --- CAMBIO AQUÍ: Adaptamos los datos para un gráfico de barras ---
    bar_chart_labels = []
    bar_chart_data = []
    for outcome_vector, count in most_common_vectors:
        bar_chart_labels.append(str(outcome_vector))
        bar_chart_data.append(count)
    
    # --- FIN DEL CAMBIO ---

    # 3. Ensamblar la respuesta JSON
    response_data = {
        "metadata": {
            "formula": "Simulación Multinomial",
            "parameters": {
                "num_experiments": num_experiments, "num_trials": num_trials,
                "probabilities": probabilities, "category_labels": labels
            }
        },
        "result": {
            "total_experiments": num_experiments,
            "unique_outcomes_count": len(vector_counts),
            "most_frequent_outcome": {"vector": str(most_frequent[0]), "count": most_frequent[1]}
        },
        # --- CAMBIO AQUÍ: La estructura de graph_data es ahora más simple ---
        "graph_data": {
            "title": "Frecuencia de Resultados de la Simulación (Top 20)",
            "labels": bar_chart_labels, # Clave 'labels' para el eje Y
            "data": bar_chart_data    # Clave 'data' para el eje X
        }
    }
    
    # Añadimos un print para que puedas verificar la nueva estructura en tu terminal de Django
    print("DEBUG: Nueva estructura de graph_data:", response_data["graph_data"])

    return response_data