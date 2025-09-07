from rest_framework import serializers
import math

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
    z_score = serializers.FloatField()

class BernoulliInputSerializer(serializers.Serializer):
    p = serializers.FloatField(min_value=0, max_value=1, help_text="Probabilidad de éxito")
    n = serializers.IntegerField(min_value=1)

class MultinomialInputSerializer(serializers.Serializer):
    n = serializers.IntegerField(min_value=1)
    k = serializers.IntegerField(min_value=1)
    probabilities = serializers.ListField(child=serializers.FloatField(min_value=0, max_value=1))
    #category_labels = serializers.ListField(child=serializers.CharField(max_length=100))

    def validate(self, data):
        k = data['k']
        probabilities = data['probabilities']
        #labels = data['category_labels']

        # 3. Verificar que la suma de las probabilidades sea 1
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