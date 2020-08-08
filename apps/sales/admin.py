from django.contrib import admin
from .models import *

# Register your models here.

class SaleAdmin(admin.ModelAdmin):
    list_display = ('type_receipt', 'num_receipt', 'serie_receipt', 'total_sale', 'client', 'created_at')  
    search_fields =  ['type_receipt', 'num_receipt', 'serie_receipt', 'client__name', 'client__lastname', 'client__dni'] 

class SaleDetailAdmin(admin.ModelAdmin):
    list_display = ('sale', 'item', 'quantity', 'discount', 'sale_price')  
    search_fields =  ['id', 'sale_price', 'sale__type_receipt', 'sale__num_receipt', 'sale__client__name', 'sale__client__lastname', 'sale__client__dni', 'item__name', 'item__brand' ] 

admin.site.register(Sale, SaleAdmin)
admin.site.register(SaleDetail, SaleDetailAdmin)
