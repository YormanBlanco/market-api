from django.urls import path, include
from rest_framework import routers

from apps.sales.views import *

router = routers.DefaultRouter()

#Registro las rutas, que viewSet ejecutara y su basename
router.register(r'sale', SaleViewSet, basename='sale')
router.register(r'saledetail', SaleDetailViewSet, basename='saledetail')

urlpatterns = [
    path('', include(router.urls)),
    #path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]