from django.db import models
from django.contrib.auth.models import User


class Producto(models.Model):
    UNIDAD_MEDIDA_CHOICES = [
        ('Unidad(u)', 'Unidad(u)'),
        ('Gramos(g)', 'Gramos(g)'),
        ('Kilogramos(kg)', 'Kilogramos(kg)'),
        ('Litros(L)', 'Litros(L)'),
        ('Mililitros(ml)', 'Mililitros(ml)')
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    cantidad_disponible = models.PositiveIntegerField()
    unidad_medida = models.CharField(max_length=15,  null=True, choices=UNIDAD_MEDIDA_CHOICES)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre

class PlatoProducto(models.Model):
    UNIDAD_MEDIDA_CHOICES = [
        ('Unidad(u)', 'Unidad(u)'),
        ('Gramos(g)', 'Gramos(g)'),
        ('Kilogramos(kg)', 'Kilogramos(kg)'),
        ('Litros(L)', 'Litros(L)'),
        ('Mililitros(ml)', 'Mililitros(ml)')
    ]

    plato = models.ForeignKey('platos.Plato', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad_necesaria = models.DecimalField(max_digits=10, decimal_places=2)  
    unidad_medida = models.CharField(max_length=15,  null=True, choices=UNIDAD_MEDIDA_CHOICES)

    def __str__(self):
        return f"{self.plato.nombre} - {self.producto.nombre}"
