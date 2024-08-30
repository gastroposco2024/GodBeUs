from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
from .choices import CONCEPTO_CATEGORIAS

class Pago(models.Model):
    METODO_PAGO_CHOICES = [
        ('Efectivo', 'Efectivo'),
        ('Consignación', 'Consignación'),
        ('Transferencia', 'Transferencia'),
        ('Cheque', 'Cheque'),
        ('Tarjeta crédito', 'Tarjeta crédito'),
        ('Tarjeta débito', 'Tarjeta débito'),
    ]
    
    IMPUESTO_CHOICES = [
        ('Ninguno', 'Ninguno'),
        ('IVA Exento (0%)', 'IVA Exento (0%)'),
        ('IVA Excluido (0%)', 'IVA Excluido (0%)'),
        ('IVA (5.00%)', 'IVA (5.00%)'),
        ('IVA (19.00%)', 'IVA (19.00%)'),
        ('IVA (8.00%)', 'IVA (8.00%)'),
    ]
    

    CONCEPTO_CHOICES = [
        (key, value) for category in CONCEPTO_CATEGORIAS.values() for (key, value) in category
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nota_egreso = models.CharField(max_length=100)
    fecha = models.DateTimeField(default=timezone.now)
    metodo_pago = models.CharField(max_length=20, choices=METODO_PAGO_CHOICES)
    observaciones = models.TextField(blank=True, null=True)
    cantidad = models.PositiveIntegerField()
    impuesto = models.CharField(max_length=20, choices=IMPUESTO_CHOICES)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    archivo_adjunto = models.FileField(upload_to='archivos_adjunto/', blank=True, null=True)
    concepto = models.CharField(max_length=100, choices=CONCEPTO_CHOICES)
    
    def valor_impuesto(self):
        """Calcula el valor del impuesto basado en el porcentaje."""
        if self.impuesto == 'Ninguno':
            return Decimal('0.00')
        elif self.impuesto == 'IVA Exento (0%)':
            return Decimal('0.00')
        elif self.impuesto == 'IVA Excluido (0%)':
            return Decimal('0.00')
        elif self.impuesto == 'IVA (5.00%)':
            return self.valor * Decimal('0.05')
        elif self.impuesto == 'IVA (19.00%)':
            return self.valor * Decimal('0.19')
        elif self.impuesto == 'IVA (8.00%)':
            return self.valor * Decimal('0.08')
        return Decimal('0.00')

    def calcular_total(self):
        """Calcula el total aplicando el impuesto correspondiente."""
        return self.valor + self.valor_impuesto()

    def __str__(self):
        return f"Pago {self.nota_egreso} - {self.fecha}"
