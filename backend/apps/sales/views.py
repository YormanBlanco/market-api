from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .models import *
from .serializers import *

# Create your views here.
class SaleViewSet(viewsets.ViewSet):
    #GET
    def list(self, request): #listar 
        queryset = Sale.objects.filter(state = True) #obtengo las q esten en True
        search = request.GET.get('search', None)
        if search is not None: #si hay una busqueda
            queryset = queryset.filter(
                Q(type_receipt = search) | Q(num_receipt = search) | Q(serie_receipt = search) |
                Q(client__name__icontains = search) | Q(client__lastname__icontains = search) | Q(client__dni__icontains = search),
                state = True
            ).distinct()
       
        serializer = SaleSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk): #obtener una sola 
        queryset = get_object_or_404(Sale.objects.all(), pk=pk) #busco la q coindia con el pk(id) q le estan pasando, si no devuelve un 404
        serializer = SaleSerializer(queryset)
        return Response(serializer.data)

    #POST
    def create(self, request): #crear una nueva 
        serializer = SaleSerializer(data = request.data)
        if serializer.is_valid(): #si los datos son validos
            serializer.save() #guardo
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #PUT
    def update(self, request, pk): 
        queryset = Sale.objects.get(pk=pk) #Obtengo la que coincide con el pk
        serializer = SaleSerializer(queryset, data=request.data)
        if serializer.is_valid(): #si los datos son validos
            serializer.save() #guardo
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #Delete
    def destroy(self, request, pk):
        queryset = Sale.objects.get(pk=pk)
        #le paso al serializer el queryset, la data a actualizar, y partial=True para indicarle que es solo ese field
        serializer = SaleSerializer(queryset, data={"state":False}, partial=True) #el state pasa a ser False
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Sale was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SaleDetailViewSet(viewsets.ViewSet):
    #GET
    def list(self, request): #listar 
        queryset = SaleDetail.objects.filter(state = True) #obtengo las q esten en True
        search = request.GET.get('search', None)
        if search is not None: #si hay una busqueda
            queryset = queryset.filter(
                Q(sale_price = search) | Q(sale__type_receipt = search) | Q(sale__num_receipt = search) |
                Q(sale__client__name__icontains = search) | Q(sale__client__lastname__icontains = search) | Q(sale__client__dni__icontains = search) | Q(item__name__icontains = search) | Q(item__brand__icontains = search),
                state = True
            ).distinct()
       
        serializer = SaleDetailSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk): #obtener una sola 
        queryset = get_object_or_404(SaleDetail.objects.all(), pk=pk) #busco la q coindia con el pk(id) q le estan pasando, si no devuelve un 404
        serializer = SaleDetailSerializer(queryset)
        return Response(serializer.data)

    #POST
    def create(self, request): #crear una nueva 
        serializer = SaleDetailSerializer(data = request.data)
        if serializer.is_valid(): #si los datos son validos
            serializer.save() #guardo
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #PUT
    def update(self, request, pk): 
        queryset = SaleDetail.objects.get(pk=pk) #Obtengo la que coincide con el pk
        serializer = SaleDetailSerializer(queryset, data=request.data)
        if serializer.is_valid(): #si los datos son validos
            serializer.save() #guardo
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #Delete
    def destroy(self, request, pk):
        queryset = SaleDetail.objects.get(pk=pk)
        #le paso al serializer el queryset, la data a actualizar, y partial=True para indicarle que es solo ese field
        serializer = SaleDetailSerializer(queryset, data={"state":False}, partial=True) #el state pasa a ser False
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Sale detail was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
