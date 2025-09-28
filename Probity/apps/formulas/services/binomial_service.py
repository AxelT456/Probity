from collections import Counter
import random

def simular(n:int,p:float, k:int)->dict:
    '''n son interaciones, p la probabilidad de exito, k son los experimentos esperados
        funcion para simular los datos
    '''
    mandar=[]
    exitos=0
    for x in range(n):
        for y in range(k):
            if random.uniform(0, 1)<p: exitos+=1
        mandar.append(exitos)
        exitos=0    
    frecuencia=Counter(mandar)  
    for valor in sorted(frecuencia.keys()):
        print(f"{valor} : {frecuencia[valor]}")
        
    return {"frecuencia":frecuencia,"secuencia":mandar}


def get_binomial_data(n: int, p: float, k:int) -> dict:
        """
        Prepara el diccionario completo con todos los datos y puntos para el grafico
        n=ensayos, p=probabilidad, k=exitos observados (aplica solo teorico)
        """
        #2.- Se preparan los puntos para el grafico
        x_points = list(range(k + 1))
        #1 Simular datos
        simulacion=simular(n,p,k)
        # 4. Ensamblar la estructura de respuesta completa
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
                "sucesion":simulacion["secuencia"],
                "frecuencia":simulacion["frecuencia"]
            },
            "graph_data": {
                "title": f"Distribución Binomial (n={n}, p={p})",
                "x_label": "Número de Éxitos (k)",
                "y_label": "Probabilidad",
                "datasets": [
                    {
                        "label": "Datos Simulados",
                        "type": "bar",
                        "x": x_points,
                        "y": simulacion["frecuencia"]
                    }
                ]
            }
        }
        return response_data