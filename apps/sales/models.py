from django.db import models
import uuid
from django.db.models import Sum, Count, FloatField, F
from django.db.models.signals import post_save
from django.dispatch import receiver
from ..entries.models import BaseModel, Item, Person, EntryDetail #importo del models de la app entries

# Create your models here.
class Sale(BaseModel):
    type_receipt = models.CharField(max_length=50, null=False)
    num_receipt = models.CharField(max_length=50, null=False)
    serie_receipt = models.CharField(max_length=50)
    tax = models.DecimalField(max_digits=4, decimal_places=2, null=False)
    client = models.ForeignKey(Person, on_delete=models.CASCADE)
    total_sale = models.DecimalField(max_digits=11, decimal_places=2, default="0.00") #total_venta

    class Meta:
        verbose_name = 'Sale'
        verbose_name_plural = 'Sales'

    def __str__(self): #Como se mostrara en el admin
        return self.type_receipt + " " + self.num_receipt 

class SaleDetail(BaseModel):
    quantity = models.IntegerField(null=False) #cantidad    
    sale_price = models.DecimalField(max_digits=11, decimal_places=2, null=False) #precio venta
    discount = models.DecimalField(max_digits=11, decimal_places=2, default="0") #descuento
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE) #idsale
    item = models.ForeignKey(Item, on_delete=models.CASCADE) #iditem

    class Meta:
        verbose_name = 'SaleDetail'
        verbose_name_plural = 'SalesDetails'

#Signals django, algo como un trigger en sql
@receiver(post_save, sender=SaleDetail)
def saleDetail_save(sender, instance, **kwargs): #cuando se guarde un saledetail se calcule el total_sale y se guarde en sale y actualice el stock del item
    sale_id = instance.sale.id
    item_id = instance.item.id

    #calcular total_sale
    sale = Sale.objects.get(pk=sale_id) 
    if sale:
        sub_total = SaleDetail.objects \
            .filter(sale=sale_id) \
            .aggregate(sub_total = Sum('sale_price')) \
            .get('sub_total',0.00) 

        discount_total = SaleDetail.objects \
            .filter(sale=sale_id) \
            .aggregate(Sum('discount')) \
            .get('discount__sum',0.00) 

        discount = (discount_total * sub_total) / 100
        sale.total_sale = sub_total - discount
        sale.save() 

    #actualizar stock
    item = Item.objects.get(pk = item_id)
    if item:
        new_stock = int(item.stock) - int(instance.quantity)
        item.stock = new_stock
        item.save() 

    #actualizar el sale_price del EntryDetail a partir del ultimo sale_price q haya tenido un item en el SaleDetail 
    entryDetail = EntryDetail.objects.filter(item = item_id)
    if entryDetail:
        sale_price = instance.sale_price
        quantity = instance.quantity
        lastSale_price = float(sale_price) / float(quantity)
        entryDetail.update(sale_price=lastSale_price)


    
