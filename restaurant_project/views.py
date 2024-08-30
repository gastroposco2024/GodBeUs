from django.shortcuts import render, redirect
from pedidos.views import  crear_pedido, home

def app(request):
    return crear_pedido(request)

def home(request):
    return home(request)
