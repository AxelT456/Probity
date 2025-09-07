from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import BinomialInputSerializer, NormalInputSerializer, BernoulliInputSerializer, MultinomialInputSerializer, GibbsInputSerializer
from .services.binomial_service import get_binomial_data
from .services.normal_service import get_normal_standard_data
from .services.bernoulli_service import get_bernoulli_data
from .services.multinomial_service import get_multinomial_data
from .services.gibbs_service import get_gibbs_data
from .services.normal_service import get_normal_cdf_data

class BinomialFormulaView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = BinomialInputSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            try:
                # Llamamos a nuestra función principal del servicio
                full_data = get_binomial_data(
                    n=validated_data['n'],
                    p=validated_data['p'],
                    k=validated_data['k']
                )
                return Response(full_data, status=status.HTTP_200_OK)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class NormalFormulaView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = NormalInputSerializer(data=request.data)
        if serializer.is_valid():
            z_score = serializer.validated_data['z_score']
            try:
                full_data = get_normal_standard_data(z_score=z_score)
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
                full_data = get_bernoulli_data(
                    p=data['p'],
                    n=data['n'] 
                )
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
                    n=data['n'],
                    k=data['k'],
                    probabilities=data['probabilities']
                    #labels=data['category_labels']
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
                # La llamada a tu servicio sigue siendo la misma
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
                    "detalle_tecnico": str(e) # Este es el mensaje exacto del error
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class NormalCumulativeView(APIView):
    def post(self, request, *args, **kwargs):
        # Usamos el mismo Serializer porque el input es el mismo
        serializer = NormalInputSerializer(data=request.data)

        if serializer.is_valid():
            z_score = serializer.validated_data['z_score']
            try:
                # Llamamos a nuestra nueva función de servicio enfocada en la CDF
                full_data = get_normal_cdf_data(z_score=z_score)
                return Response(full_data, status=status.HTTP_200_OK)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)