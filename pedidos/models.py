from django.db import models
from django.contrib.auth.models import User
from mesas.models import Mesa
from platos.models import Plato
from inventario.models import Producto, PlatoProducto
from django.db.models.signals import post_save
import datetime
from django.dispatch import receiver

class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE)
    fecha_pedido = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido {self.id} - Mesa {self.mesa.numero} - {self.fecha_pedido}"

class ItemPedido(models.Model):
    ESTADO_CHOICES = [
        ('En proceso', 'En proceso'),
        ('Entregado', 'Entregado'),
    ]

    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    plato = models.ForeignKey(Plato, on_delete=models.CASCADE, null=True, blank=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True, blank=True)
    cantidad = models.PositiveIntegerField()
    detalle = models.CharField(max_length=200)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='En proceso')
    created_at = models.DateTimeField(default=datetime.datetime.now)
    notificado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.plato.nombre if self.plato else self.producto.nombre} - Cantidad: {self.cantidad} - Estado: {self.estado}"

    @property
    def total(self):
        # Calcula el total en función del plato o producto
        precio = self.plato.precio if self.plato else self.producto.precio
        return precio * self.cantidad

class PedidoDomicilio(models.Model):
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('En camino', 'En camino'),
        ('Entregado', 'Entregado'),
        ('Facturado', 'Facturado'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    doc_cliente = models.PositiveIntegerField()
    nombre_cliente = models.CharField(max_length=50)
    telefono_cliente = models.CharField(max_length=50)
    direccion_cliente = models.CharField(max_length=100)
    estado_pedido = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Pendiente')
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    fecha_estado_actualizacion = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"Pedido {self.id} - {self.doc_cliente} - {self.fecha_pedido}"

class ItemPedidoDomicilio(models.Model):
    ESTADO_CHOICES = [
        ('En proceso', 'En proceso'),
        ('Entregado', 'Entregado'),
    ]

    pedido = models.ForeignKey(PedidoDomicilio, on_delete=models.CASCADE)
    plato = models.ForeignKey(Plato, on_delete=models.CASCADE, null=True, blank=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True, blank=True)
    cantidad = models.PositiveIntegerField()
    detalle = models.CharField(max_length=200)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='En proceso')

    def __str__(self):
        return f"{self.plato.nombre if self.plato else self.producto.nombre} - Cantidad: {self.cantidad} - Estado: {self.estado}"
