from django.db import models
import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver
from ..entries.models import BaseModel, Item, Person #importo del models de la app entries

# Create your models here.
class Sale(BaseModel):
    type_receipt = models.CharField(max_length=50, null=False)
    num_receipt = models.CharField(max_length=50, null=False)
    serie_receipt = models.CharField(max_length=50)
    tax = models.DecimalField(max_digits=4, decimal_places=2, null=False)
    client = models.ForeignKey(Person, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Sale'
        verbose_name_plural = 'Sales'

    def __str__(self): #Como se mostrara en el admin
        return self.type_receipt + " " + self.num_receipt 

class SaleDetail(BaseModel):
    quantity = models.IntegerField(null=False) #cantidad    
    sale_price = models.DecimalField(max_digits=11, decimal_places=2, null=False) #precio venta
    discount = models.DecimalField(max_digits=11, decimal_places=2, null=False) #descuento
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE) #idsale
    item = models.ForeignKey(Item, on_delete=models.CASCADE) #iditem

    class Meta:
        verbose_name = 'SaleDetail'
        verbose_name_plural = 'SalesDetail'

#Signals django, algo como un trigger en sql
@receiver(post_save, sender=SaleDetail)
def subtract_stock(sender, instance, **kwargs): #cuando se guarde un saledetail se reste el stock del item, 
    item_id = instance.item.id
    item = Item.objects.get(pk = item_id)
    item.stock -= instance.quantity
    item.save() 

    
