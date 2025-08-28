# test_graficas.py
import os
import django
import matplotlib.pyplot as plt

# --- Bloque de Configuración de Django ---
# Esencial para que el script sepa de tu proyecto
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Probity.settings')
django.setup()
# -----------------------------------------

# Ahora que Django está configurado, podemos importar nuestros servicios
from apps.formulas.services.binomial_service import get_binomial_data

def probar_grafico_binomial():
    """
    Esta función prueba la lógica de la binomial y muestra el gráfico.
    """
    # 1. Define los parámetros de prueba
    n_test = 80
    p_test = 0.6
    k_test = 10
    print(f"Probando la función binomial con n={n_test}, p={p_test}, k={k_test}...")

    # 2. Llama a la función del servicio (igual que lo haría la vista)
    datos_completos = get_binomial_data(n=n_test, p=p_test, k=k_test)

    # 3. Imprime los resultados numéricos para verificarlos
    print("\n--- Resultados Numéricos ---")
    print(datos_completos['result'])

    # 4. Extrae los datos del gráfico y visualízalos con Matplotlib
    print("\nGenerando gráfico...")
    graph_data = datos_completos['graph_data']

    # Extraemos los datos de las barras (PMF)
    pmf_dataset = graph_data['datasets'][0]
    x_values = pmf_dataset['x']
    y_values_pmf = pmf_dataset['y']

    # Extraemos los datos de la línea (CDF)
    cdf_dataset = graph_data['datasets'][1]
    y_values_cdf = cdf_dataset['y']

    # Creamos la figura y los ejes
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Graficamos las barras (PMF)
    ax1.bar(x_values, y_values_pmf, color='skyblue', label='Probabilidad Puntual (PMF)')
    ax1.set_xlabel(graph_data['x_label'])
    ax1.set_ylabel(graph_data['y_label'], color='skyblue')
    ax1.tick_params(axis='y', labelcolor='skyblue')

    # Creamos un segundo eje Y para la línea (CDF)
    ax2 = ax1.twinx()
    ax2.plot(x_values, y_values_cdf, color='red', marker='o', linestyle='--', label='Probabilidad Acumulada (CDF)')
    ax2.set_ylabel('Probabilidad Acumulada', color='red')
    ax2.tick_params(axis='y', labelcolor='red')

    plt.title(graph_data['title'])
    fig.tight_layout()

    # 5. Muestra la ventana del gráfico en tu pantalla
    plt.show()

# --- Ejecutar la prueba ---
if __name__ == '__main__':
    probar_grafico_binomial()