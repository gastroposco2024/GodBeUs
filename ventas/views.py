# ventas/views.py
from django.shortcuts import render
from .models import Compra

def obtener_registros_venta(request):
    compras = Compra.objects.all()
    return render(request, 'ventas/obtener_registros_venta.html', {'compras': compras})
