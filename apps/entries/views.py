from rest_framework import viewsets 
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
import cloudinary.uploader
import cloudinary

from .models import *
from .serializers import *

# Create your views here.
class CategoryViewSet(viewsets.ViewSet):
    #GET
    def list(self, request): #listar 
        queryset = Category.objects.filter(state = True) #obtengo las q esten en True
        search = request.GET.get('search', None)
        if search is not None: #si hay una busqueda
            queryset = queryset.filter(
                Q(name__icontains = search),
                state = True
            ).distinct() 
       
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk): #obtener una sola 
        queryset = get_object_or_404(Category.objects.all(), pk=pk) #busco la q coindia con el pk(id) q le estan pasando, si no devuelve un 404
        serializer = CategorySerializer(queryset)
        return Response(serializer.data)

    #POST
    def create(self, request): #crear una nueva 
        serializer = CategorySerializer(data = request.data)
        if serializer.is_valid(): #si los datos son validos
            serializer.save() #guardo
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #PUT
    def update(self, request, pk): 
        queryset = Category.objects.get(pk=pk) #Obtengo la que coincide con el pk
        serializer = CategorySerializer(queryset, data=request.data)
        if serializer.is_valid(): #si los datos son validos
            serializer.save() #guardo
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #Delete
    def destroy(self, request, pk):
        queryset = Category.objects.get(pk=pk)
        #le paso al serializer el queryset, la data a actualizar, y partial=True para indicarle que es solo ese field
        serializer = CategorySerializer(queryset, data={"state":False}, partial=True) #el state pasa a ser False
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Category was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ItemViewSet(viewsets.ViewSet):
    #GET
    def list(self, request): #listar 
        queryset = Item.objects.filter(state = True) #obtengo las q esten en True
        search = request.GET.get('search', None)
        if search is not None: #si hay una busqueda
            queryset = queryset.filter(
                Q(name__icontains = search) | Q(stock__icontains = search) | Q(category__name__icontains = search) |
                Q(brand__icontains = search) | Q(packaging__icontains = search) | Q(gramsOrMilliliters__icontains = search),
                state = True
            ).distinct()
       
        serializer = ItemSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk): #obtener una sola 
        queryset = get_object_or_404(Item.objects.all(), pk=pk) #busco la q coindia con el pk(id) q le estan pasando, si no devuelve un 404
        serializer = ItemSerializer(queryset)
        return Response(serializer.data)

    #POST
    def create(self, request): #crear una nueva 
        image = request.data.get('image') #obtengo la image del request
        upload = cloudinary.uploader.upload(image).get('public_id') #subo la image a cloudinary y obtengo el public_id
        serializer = ItemSerializer(
            data = {
                "brand":request.data.get('brand'),
                "name":request.data.get('name'),
                "description":request.data.get('description'),
                "stock":request.data.get('stock'),
                "image":upload,
                "packaging": request.data.get('packaging'),
                "gramsOrMilliliters": request.data.get('gramsOrMilliliters'),
                "category": request.data.get('category')
            }   
        ) 
        if serializer.is_valid(): #si los datos son validos
            serializer.save() #guardo
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #PUT
    def update(self, request, pk):  
        image = request.data.get('image') #obtengo la image del request
        queryset = Item.objects.get(pk=pk) #Obtengo la que coincide con el pk
        if ((queryset.image is not None) and (queryset.image is not image)): #si hay una imagen y no es la misma q trae el request
            cloudinary.uploader.destroy(queryset.image.public_id, invalidate=True) #elimino la antigua imagen de cloudinary
        upload = cloudinary.uploader.upload(image).get('public_id') #subo la nueva image a cloudinary y obtengo el public_id
        serializer = ItemSerializer(
            queryset, 
            data = {
                "state": request.data.get('state'),
                "brand": request.data.get('brand'),
                "name": request.data.get('name'),
                "description": request.data.get('description'),
                "stock": request.data.get('stock'),
                "image": upload,
                "packaging": request.data.get('packaging'),
                "gramsOrMilliliters": request.data.get('gramsOrMilliliters'),
                "category": request.data.get('category')
            }
        )
        if serializer.is_valid(): #si los datos son validos
            serializer.save() #guardo
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #Delete
    def destroy(self, request, pk):
        queryset = Item.objects.get(pk=pk)
        #le paso al serializer el queryset, la data a actualizar, y partial=True para indicarle que son solo esos fields
        serializer = ItemSerializer(queryset, data={"state":False, "image":None}, partial=True) #el state pasa a ser False, y el image vacio
        if serializer.is_valid():
            cloudinary.uploader.destroy(queryset.image.public_id, invalidate=True) #elimino la imagen de cloudinary
            serializer.save()
            return Response({'message': 'Item was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProviderViewSet(viewsets.ViewSet):
    #GET
    def list(self, request): #listar 
        queryset = Person.objects.filter(state = True, type_person='Provider') #obtengo las q esten en True
        search = request.GET.get('search', None)
        if search is not None: #si hay una busqueda
            queryset = queryset.filter(
                Q(name__icontains = search) | Q(lastname__icontains = search) | Q(dni__icontains = search) |
                Q(tlf__icontains = search) | Q(email__icontains = search),
                state = True, type_person='Provider'
            ).distinct() 
       
        serializer = PersonSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk): #obtener una sola 
        queryset = get_object_or_404(Person.objects.all(), pk=pk) #busco la q coindia con el pk(id) q le estan pasando, si no devuelve un 404
        serializer = PersonSerializer(queryset)
        return Response(serializer.data)

    #POST
    def create(self, request): #crear una nueva 
        serializer = PersonSerializer(data = request.data)
        if serializer.is_valid(): #si los datos son validos
            serializer.save() #guardo
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #PUT
    def update(self, request, pk): 
        queryset = Person.objects.get(pk=pk) #Obtengo la que coincide con el pk
        serializer = PersonSerializer(queryset, data=request.data)
        if serializer.is_valid(): #si los datos son validos
            serializer.save() #guardo
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #Delete
    def destroy(self, request, pk):
        queryset = Person.objects.get(pk=pk)
        #le paso al serializer el queryset, la data a actualizar, y partial=True para indicarle que es solo ese field
        serializer = PersonSerializer(queryset, data={"state":False}, partial=True) #el state pasa a ser False
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Provider was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClientViewSet(viewsets.ViewSet):
    #GET
    def list(self, request): #listar 
        queryset = Person.objects.filter(state = True, type_person='Client') #obtengo las q esten en True
        search = request.GET.get('search', None)
        if search is not None: #si hay una busqueda
            queryset = queryset.filter(
                Q(name__icontains = search) | Q(lastname__icontains = search) | Q(dni__icontains = search) |
                Q(tlf__icontains = search) | Q(email__icontains = search),
                state = True, type_person='Client'
            ).distinct() 
       
        serializer = PersonSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk): #obtener una sola 
        queryset = get_object_or_404(Person.objects.all(), pk=pk) #busco la q coindia con el pk(id) q le estan pasando, si no devuelve un 404
        serializer = PersonSerializer(queryset)
        return Response(serializer.data)

    #POST
    def create(self, request): #crear una nueva 
        serializer = PersonSerializer(data = request.data)
        if serializer.is_valid(): #si los datos son validos
            serializer.save() #guardo
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #PUT
    def update(self, request, pk): 
        queryset = Person.objects.get(pk=pk) #Obtengo la que coincide con el pk
        serializer = PersonSerializer(queryset, data=request.data)
        if serializer.is_valid(): #si los datos son validos
            serializer.save() #guardo
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #Delete
    def destroy(self, request, pk):
        queryset = Person.objects.get(pk=pk)
        #le paso al serializer el queryset, la data a actualizar, y partial=True para indicarle que es solo ese field
        serializer = PersonSerializer(queryset, data={"state":False}, partial=True) #el state pasa a ser False
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Provider was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EntryViewSet(viewsets.ViewSet):
    #GET
    def list(self, request): #listar 
        queryset = Entry.objects.filter(state = True) #obtengo las q esten en True
        search = request.GET.get('search', None)
        if search is not None: #si hay una busqueda
            queryset = queryset.filter(
                Q(type_receipt__icontains = search) | Q(num_receipt = search) | Q(serie_receipt = search) |
                Q(provider__name__icontains = search) | Q(provider__lastname__icontains = search) | Q(provider__dni__icontains = search),
                state = True
            ).distinct()
       
        serializer = EntrySerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk): #obtener una sola 
        queryset = get_object_or_404(Entry.objects.all(), pk=pk) #busco la q coindia con el pk(id) q le estan pasando, si no devuelve un 404
        serializer = EntrySerializer(queryset)
        return Response(serializer.data)

    #POST
    def create(self, request): #crear una nueva 
        serializer = EntrySerializer(data = request.data)
        if serializer.is_valid(): #si los datos son validos
            serializer.save() #guardo
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #PUT
    def update(self, request, pk): 
        queryset = Entry.objects.get(pk=pk) #Obtengo la que coincide con el pk
        serializer = EntrySerializer(queryset, data=request.data)
        if serializer.is_valid(): #si los datos son validos
            serializer.save() #guardo
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #Delete
    def destroy(self, request, pk):
        queryset = Entry.objects.get(pk=pk)
        #le paso al serializer el queryset, la data a actualizar, y partial=True para indicarle que es solo ese field
        serializer = EntrySerializer(queryset, data={"state":False}, partial=True) #el state pasa a ser False
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Entry was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EntryDetailViewSet(viewsets.ViewSet):
    #GET
    def list(self, request): #listar 
        queryset = EntryDetail.objects.filter(state = True) #obtengo las q esten en True
        search = request.GET.get('search', None)
        if search is not None: #si hay una busqueda
            queryset = queryset.filter(
                Q(purchase_price__icontains = search) | Q(sale_price__icontains = search) |
                Q(entry__provider__name__icontains = search) | Q(entry__provider__lastname__icontains = search) | Q(entry__provider__dni__icontains = search) |Q(item__name__icontains = search) | Q(item__brand__icontains = search),
                state = True
            ).distinct()
       
        serializer = EntryDetailSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk): #obtener una sola 
        queryset = get_object_or_404(EntryDetail.objects.all(), pk=pk) #busco la q coindia con el pk(id) q le estan pasando, si no devuelve un 404
        serializer = EntryDetailSerializer(queryset)
        return Response(serializer.data)

    #POST
    def create(self, request): #crear una nueva 
        serializer = EntryDetailSerializer(data = request.data)
        if serializer.is_valid(): #si los datos son validos
            serializer.save() #guardo
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

    #PUT
    def update(self, request, pk): 
        queryset = EntryDetail.objects.get(pk=pk) #Obtengo la que coincide con el pk
        serializer = EntryDetailSerializer(queryset, data=request.data)
        if serializer.is_valid(): #si los datos son validos
            serializer.save() #guardo
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #Delete
    def destroy(self, request, pk):
        queryset = EntryDetail.objects.get(pk=pk)
        #le paso al serializer el queryset, la data a actualizar, y partial=True para indicarle que es solo ese field
        serializer = EntryDetailSerializer(queryset, data={"state":False}, partial=True) #el state pasa a ser False
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Entry detail was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)