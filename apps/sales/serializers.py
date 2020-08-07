from rest_framework import serializers
from .models import *
from ..entries.serializers import PersonSerializer 
from ..entries.models import Person 

#create your serializers here.

class SaleSerializer(serializers.ModelSerializer):
    client = PersonSerializer(read_only = True) #obtener objt client 
    clientid = serializers.PrimaryKeyRelatedField(write_only=True, queryset = Person.objects.filter(type_person='Client', state=True), source='client') #para guardar solo el id del client

    class Meta:
        model = Sale
        fields = ('id','state','type_receipt', 'num_receipt', 'serie_receipt', 'tax', 'created_at', 'updated_at', 'deleted_at', 'client', 'clientid') 

class SaleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleDetail
        fields = '__all__' #__all__ para indicar q debe serializar todos los atributos del modelo