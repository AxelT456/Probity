from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# --- Importaciones de Serializers ---
from .serializers import (
    BinomialInputSerializer,
    NormalInputSerializer,
    BernoulliInputSerializer,
    MultinomialInputSerializer,
    GibbsInputSerializer,
    ExponencialInputSerializer # Asegúrate de que este exista en serializers.py
)

# --- Importaciones de Services ---
from .services.binomial_service import get_binomial_data
from .services.normal_service import get_normal_distribution_data
from .services.bernoulli_service import get_bernoulli_data
from .services.multinomial_service import get_multinomial_data
from .services.gibbs_service import get_gibbs_data
from .services.exponencial_service import get_exponencial_data # Asegúrate de que este servicio exista
from django.conf import settings

print(settings.GEMINI_API_KEY)  # Para probar que sí lo carga

# --- Vistas de la API ---

class BinomialFormulaView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = BinomialInputSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            try:
                full_data = get_binomial_data(n=data['n'], p=data['p'], k=data['k'])
                return Response(full_data, status=status.HTTP_200_OK)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NormalFormulaView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = NormalInputSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            try:
                full_data = get_normal_distribution_data(
                    mean=data['mean'],
                    std_dev=data['std_dev'],
                    x_value=data['x_value']
                )
                return Response(full_data, status=status.HTTP_200_OK)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BernoulliFormulaView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = BernoulliInputSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            try:
                full_data = get_bernoulli_data(p=data['p'], n=data['n'])
                return Response(full_data, status=status.HTTP_200_OK)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MultinomialFormulaView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = MultinomialInputSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            try:
                full_data = get_multinomial_data(
                    num_experiments=data['num_experiments'],
                    num_trials=data['num_trials'],
                    probabilities=data['probabilities'],
                    labels=data['category_labels']
                )
                return Response(full_data, status=status.HTTP_200_OK)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GibbsFormulaView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = GibbsInputSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            try:
                full_data = get_gibbs_data(
                    limite_inferior=data['limite_inferior'],
                    limite_superior=data['limite_superior'],
                    x0=data['x0'],
                    y0=data['y0'],
                    iteraciones=data['iteraciones'],
                    formula=data['formula']
                )
                return Response(full_data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({
                    "error": "Ocurrió un error inesperado durante el cálculo.",
                    "detalle_tecnico": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ExponencialFormulaView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ExponencialInputSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            try:
                full_data = get_exponencial_data(
                    n=validated_data['n'],
                    rate=validated_data['rate'] # Usando el nombre de campo actualizado
                )
                return Response(full_data, status=status.HTTP_200_OK)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
