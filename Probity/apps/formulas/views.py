from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import BinomialInputSerializer # Asegúrate de que este serializer exista
from .services.binomial_service import get_binomial_data

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
    
class BernoulliFormulaView(APIView):
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