from rest_framework import serializers
from .models import *


#create your serializers here.

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__' #__all__ para indicar q debe serializar todos los atributos del modelo

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__' #__all__ para indicar q debe serializar todos los atributos del modelo

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__' #__all__ para indicar q debe serializar todos los atributos del modelo


class EntrySerializer(serializers.ModelSerializer):
    provider = PersonSerializer(read_only = True)
    providerid = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Person.objects.filter(type_person='Provider', state=True), source='provider')

    class Meta:
        model = Entry
        fields = ('id','state','type_receipt', 'num_receipt', 'serie_receipt', 'tax', 'created_at', 'updated_at', 'deleted_at', 'provider', 'providerid') 

class EntryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntryDetail
        fields = '__all__' #__all__ para indicar q debe serializar todos los atributos del modelo