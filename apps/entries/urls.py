from django.urls import path, include
from rest_framework import routers

from apps.entries.views import *

router = routers.DefaultRouter()

#Registro las rutas, que viewSet ejecutara y su basename
router.register(r'category', CategoryViewSet, basename='category')
router.register(r'provider', ProviderViewSet, basename='provider')
router.register(r'client', ClientViewSet, basename='client')
router.register(r'item', ItemViewSet, basename='item')
router.register(r'entry', EntryViewSet, basename='entry')
router.register(r'entrydetail', EntryDetailViewSet, basename='entrydetail')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]