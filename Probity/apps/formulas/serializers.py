from rest_framework import serializers
import math

class ExponencialInputSerializer(serializers.Serializer):
    n = serializers.IntegerField(min_value=1, help_text="Número de simulaciones")
    rate = serializers.FloatField(help_text="Tasa Lambda (λ), debe ser positiva")

    def validate_rate(self, value):
        if value <= 0:
            raise serializers.ValidationError("La tasa Lambda (λ) debe ser un número positivo.")
        return value

class BinomialInputSerializer(serializers.Serializer):
    """
    Este serializador valida los datos de entrada para la fórmula binomial.
    """
    n = serializers.IntegerField(min_value=1, help_text="Número de ensayos")
    p = serializers.FloatField(min_value=0, max_value=1, help_text="Probabilidad de éxito")
    k = serializers.IntegerField(min_value=0, help_text="Número de éxitos deseados")

    def validate(self, data):
        if data['k'] > data['n']:
            raise serializers.ValidationError("k (éxitos) no puede ser mayor que n (ensayos).")
        return data
    
class NormalInputSerializer(serializers.Serializer):
    mean = serializers.FloatField(help_text="Media (μ) de la distribución")
    std_dev = serializers.FloatField(min_value=0.00001, help_text="Desviación estándar (σ), debe ser positiva")
    x_value = serializers.FloatField(help_text="Punto X a evaluar")

class BernoulliInputSerializer(serializers.Serializer):
    p = serializers.FloatField(min_value=0, max_value=1, help_text="Probabilidad de éxito")
    n = serializers.IntegerField(min_value=1)

class MultinomialInputSerializer(serializers.Serializer):
    num_experiments = serializers.IntegerField(min_value=1, help_text="Número de simulaciones a correr")
    num_trials = serializers.IntegerField(min_value=1, help_text="Número de ensayos por experimento (ej. lanzamientos de dado)")
    probabilities = serializers.ListField(child=serializers.FloatField(min_value=0, max_value=1))
    category_labels = serializers.ListField(child=serializers.CharField(max_length=100))

    def validate(self, data):
        probabilities = data['probabilities']
        labels = data['category_labels']

        # Validar que las listas de probabilidades y etiquetas tengan el mismo tamaño
        if len(probabilities) != len(labels):
            raise serializers.ValidationError("Las listas 'probabilities' y 'category_labels' deben tener el mismo tamaño.")

        # Validar que la suma de las probabilidades sea 1
        if not math.isclose(sum(probabilities), 1.0):
            raise serializers.ValidationError(f"La suma de 'probabilities' ({sum(probabilities)}) debe ser igual a 1.")

        return data
    
class GibbsInputSerializer(serializers.Serializer):
    limite_inferior = serializers.IntegerField()
    limite_superior = serializers.IntegerField()
    x0 = serializers.IntegerField()
    y0 = serializers.IntegerField()
    iteraciones = serializers.IntegerField(min_value=1)
    formula = serializers.CharField()

    def validate(self, data):
        # Validaciones personalizadas
        #validar limites 
        if data['limite_inferior'] >= data['limite_superior']:
            raise serializers.ValidationError("El 'limite_inferior' debe ser menor que el 'limite_superior'.")
        if data['limite_inferior'] < 0 or data['limite_superior'] < 0:
            raise serializers.ValidationError("Los límites deben ser números enteros no negativos.")
        #validar puntos iniciales
        if data['x0'] < data['limite_inferior'] or data['x0'] > data['limite_superior']:
            raise serializers.ValidationError("'x0' debe estar dentro de los límites especificados.")
        if data['y0'] < data['limite_inferior'] or data['y0'] > data['limite_superior']:
            raise serializers.ValidationError("'y0' debe estar dentro de los límites especificados.")
        #validar existencia de la formula
        if not data['formula']:
            raise serializers.ValidationError("La 'formula' no puede estar vacía.")
        #validar iteraciones
        if data['iteraciones'] <= 0:
            raise serializers.ValidationError("'iteraciones' debe ser un entero positivo.")
        
        return data
    

class BivariateNormalInputSerializer(serializers.Serializer):
    mean_x = serializers.FloatField()
    mean_y = serializers.FloatField()
    std_dev_x = serializers.FloatField()
    std_dev_y = serializers.FloatField()
    correlation = serializers.FloatField(min_value=-1.0, max_value=1.0)
    x_value = serializers.FloatField()
    y_value = serializers.FloatField()

    def validate_std_dev_x(self, value):
        if value <= 0:
            raise serializers.ValidationError("La desviación estándar debe ser positiva.")
        return value

    def validate_std_dev_y(self, value):
        if value <= 0:
            raise serializers.ValidationError("La desviación estándar debe ser positiva.")
        return value