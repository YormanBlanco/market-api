from django.contrib import admin

from .models import *

# Register your models here.

""" AdminConfig """

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')  
    search_fields =  ['name'] 

class ItemAdmin(admin.ModelAdmin):
    list_display = ('brand', 'name', 'packaging', 'stock', 'category', 'gramsOrMilliliters' )  
    search_fields =  ['name', 'brand', 'category__name', 'gramsOrMilliliters', 'packaging'] 

class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'lastname', 'dni', 'type_person', 'tlf', 'email')  
    search_fields =  ['name', 'lastname', 'dni', 'type_person', 'tlf', 'email'] 

class EntryAdmin(admin.ModelAdmin):
    list_display = ('type_receipt', 'num_receipt', 'serie_receipt', 'provider')  
    search_fields =  ['type_receipt', 'num_receipt', 'serie_receipt', 'provider__name', 'provider__lastname', 'provider__dni'] 

class EntryDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'entry', 'item', 'quantity', 'purchase_price', 'sale_price')  
    search_fields =  ['id', 'purchase_price', 'sale_price', 'entry__provider__name', 'entry__provider__lastname', 'entry__provider__dni', 'item__name', 'item__brand' ] 



admin.site.register(Category, CategoryAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Entry, EntryAdmin)
admin.site.register(EntryDetail, EntryDetailAdmin) 