# ventas/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('obtener_registros_venta/', views.obtener_registros_venta, name='obtener_registros_venta'),
]
