from django.db import models
import uuid
from cloudinary.models import CloudinaryField
from django.db.models.signals import post_save
from django.db.models import Sum
from django.dispatch import receiver


# Create your models here.
class BaseModel(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    state = models.BooleanField('State', default = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=True) 

    class Meta:
        abstract = True #Para que cuando migre mis models a la BD, no se registre esta clase, pero si regustren los atributos de esta clase a aquellas clases q hereden de esta

class Category(BaseModel):
    name = models.CharField(max_length=45, null=False)
    description = models.CharField(max_length=450, null=False)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categorys'

    def __str__(self): #Como se mostrara en el admin
        return self.name 

class Item(BaseModel):
    brand = models.CharField(max_length=45, null=False, default=None)
    name = models.CharField(max_length=45, null=False)
    description = models.CharField(max_length=450, null=False)
    stock = models.IntegerField(default=0)
    image = CloudinaryField('image', null=True)
    packaging = models.CharField(max_length=45,null=False, default=None)
    gramsOrMilliliters = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=None)
    category = models.ForeignKey(Category, on_delete=models.CASCADE) #idcategory

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'

    def __str__(self): #Como se mostrara en el admin
        return self.brand +' '+ self.name +' '+ self.packaging 

class Person(BaseModel):
    name = models.CharField(max_length=50, null=False)
    lastname = models.CharField(max_length=50, null=False)
    dni = models.CharField(max_length=50, null=False)
    type_person = models.CharField(max_length=50, null=False)
    address = models.CharField(max_length=450, null=False)
    tlf = models.CharField(max_length=15, null=False)
    email = models.EmailField(null=False, max_length=254)

    class Meta:
        verbose_name = 'Person'
        verbose_name_plural = 'Persons'

    def __str__(self): #Como se mostrara en el admin
        return self.name + " " + self.lastname + " " + self.dni

class Entry(BaseModel):
    type_receipt = models.CharField(max_length=50, null=False)
    num_receipt = models.CharField(max_length=50, null=False)
    serie_receipt = models.CharField(max_length=50)
    tax = models.DecimalField(max_digits=4, decimal_places=2, null=False)
    provider = models.ForeignKey(Person, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Entry'
        verbose_name_plural = 'Entries'

    def __str__(self): #Como se mostrara en el admin
        return self.type_receipt + " " + self.num_receipt 

class EntryDetail(BaseModel):
    quantity = models.IntegerField(null=False) #cantidad
    purchase_price = models.DecimalField(max_digits=11, decimal_places=2, null=False) #precio compra
    sale_price = models.DecimalField(max_digits=11, decimal_places=2, null=False) #precio venta
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE) #identry
    item = models.ForeignKey(Item, on_delete=models.CASCADE) #iditem

    class Meta:
        verbose_name = 'EntryDetail'
        verbose_name_plural = 'EntriesDetail'

    #def __str__(self): #Como se mostrara en el admin
        #return self.id

#Signals django, algo como un trigger en sql
@receiver(post_save, sender=EntryDetail)
def add_stock(sender, instance, **kwargs): #cuando se guarde un entrydetail se actualice el stock del item
    item_id = instance.item.id
    item = Item.objects.get(pk = item_id)
    item.stock += instance.quantity
    item.save() 
