from .utils import combinations
import math  
#Ver tema de la simlacion
def calculate_binomial_pmf(n:int, p:float, k:int) -> float:
    """
    Calcula la Función de Masa de Probabilidad (Puntual) para P(X=k)
    Esta es la probabilidad de obtener exactamente 'k' exitos
    """
    if not(0<= p <=1):
        raise ValueError("La probabilidad p debe estar entre 0 y 1")
    # Fórmula: C(n,k) * p^k * (1-p)^(n-k)
    return combinations(n,k) * (p**k) * ((1-p)**(n-k))


def calculate_binomial_cdf(n: int, p:float, k:int)-> float:
    """
    Calcula la Función de Distribución Acumulada (CDF) para P(X<=k).
    Esta es la probabilidad de obtener 'k' exitos o menos
    """
    cumulative_prob = 0.0
    for i in range(k+1):
        cumulative_prob += calculate_binomial_pmf(n, p, i)
    return cumulative_prob


def get_binomial_data(n: int, p: float, k:int) -> dict:
        """
        Prepara el diccionario completo con todos los datos y puntos para el grafico
        """
        #1.- Se calculan los resultados para el 'k' daddo
        pmf_at_k = calculate_binomial_pmf(n, p, k)
        cdf_at_k = calculate_binomial_cdf(n, p, k)
        mean = n * p
        variance = n * p * (1 - p)

        #2.- Se preparan los puntos para el grafico
        x_points = list(range(n + 1))
        pmf_all_points = [calculate_binomial_pmf(n,p,i) for i in x_points]
        cdf_all_points = [calculate_binomial_cdf(n,p,i) for i in x_points]
        
        # 3. Ensamblar la estructura de respuesta completa
        response_data = {
            "metadata": {
                "formula": "Binomial",
                "parameters": { 
                     "n": n,
                     "p": p, 
                     "k": k 
                     }
            },
            "result": {
                "pmf_at_k": pmf_at_k,
                "cdf_at_k": cdf_at_k,
                "mean": mean,
                "variance": variance
            },
            "graph_data": {
                "title": f"Distribución Binomial (n={n}, p={p})",
                "x_label": "Número de Éxitos (k)",
                "y_label": "Probabilidad",
                "datasets": [
                    {
                        "label": "Probabilidad Puntual (PMF)",
                        "type": "bar",
                        "x": x_points,
                        "y": pmf_all_points
                    },
                    {
                        "label": "Probabilidad Acumulada (CDF)",
                        "type": "line",
                        "x": x_points,
                        "y": cdf_all_points
                    }
                ]
            }
        }
        return response_data