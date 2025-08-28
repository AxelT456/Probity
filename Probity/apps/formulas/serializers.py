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

class MultinomialInputSerializer(serializers.Serializer):
    n = serializers.IntegerField(min_value=1)
    outcomes = serializers.ListField(child=serializers.IntegerField(min_value=0))
    probabilities = serializers.ListField(child=serializers.FloatField(min_value=0, max_value=1))
    category_labels = serializers.ListField(child=serializers.CharField(max_length=100))

    def validate(self, data):
        outcomes = data['outcomes']
        probabilities = data['probabilities']
        labels = data['category_labels']

        # 1. Verificar que las listas tengan el mismo tamaño
        if not (len(outcomes) == len(probabilities) == len(labels)):
            raise serializers.ValidationError("Las listas 'outcomes', 'probabilities' y 'category_labels' deben tener el mismo número de elementos.")

        # 2. Verificar que la suma de los resultados sea igual a n
        if sum(outcomes) != data['n']:
            raise serializers.ValidationError(f"La suma de 'outcomes' ({sum(outcomes)}) debe ser igual a 'n' ({data['n']}).")

        # 3. Verificar que la suma de las probabilidades sea 1
        if not math.isclose(sum(probabilities), 1.0):
            raise serializers.ValidationError(f"La suma de 'probabilities' ({sum(probabilities)}) debe ser igual a 1.")

        return data