from django.db import models
from django.contrib.auth.models import User
from mesas.models import Mesa
from pedidos.models import Pedido
from platos.models import Plato 
from decimal import Decimal

class Compra(models.Model):
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

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    tipo_pago = models.CharField(max_length=20, choices=METODO_PAGO_CHOICES)
    cedula_cliente = models.CharField(max_length=20)
    fecha_compra = models.DateTimeField(auto_now_add=True)
    impuesto = models.CharField(max_length=20, choices=IMPUESTO_CHOICES, default='Ninguno')
    total_impuesto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valor_impuesto = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def valor_impuesto(self):
        """Calcula el valor del impuesto basado en el porcentaje."""
        if self.impuesto == 'Ninguno':
            return Decimal('0.00')
        elif self.impuesto == 'IVA Exento (0%)':
            return Decimal('0.00')
        elif self.impuesto == 'IVA Excluido (0%)':
            return Decimal('0.00')
        elif self.impuesto == 'IVA (5.00%)':
            return self.total * Decimal('0.05')
        elif self.impuesto == 'IVA (19.00%)':
            return self.total * Decimal('0.19')
        elif self.impuesto == 'IVA (8.00%)':
            return self.total * Decimal('0.08')
        return Decimal('0.00')

    def total_con_impuesto(self):
        """Calcula el total aplicando el impuesto correspondiente."""
        self.valor_impuesto = self.valor_impuesto()
        total = self.total + self.valor_impuesto
        self.total_impuesto = total
        
        return total

    def __str__(self):
        return f"Compra {self.id} - Mesa {self.mesa.numero} - {self.fecha_compra}"

class CompraDetalle(models.Model):
    compra = models.ForeignKey('ventas.Compra', on_delete=models.CASCADE, related_name='detalles')
    plato = models.ForeignKey('platos.Plato', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return f"Compra {self.compra.id} - Plato: {self.plato.nombre} - Cantidad: {self.cantidad}"

class CompraDomicilio(models.Model):
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
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    tipo_pago = models.CharField(max_length=20, choices=METODO_PAGO_CHOICES)
    cedula_cliente = models.CharField(max_length=20)
    nombre_cliente = models.CharField(max_length=20)
    telefono_cliente = models.CharField(max_length=20)
    direccion_cliente = models.CharField(max_length=50)
    fecha_compra = models.DateTimeField(auto_now_add=True)
    impuesto = models.CharField(max_length=20, choices=IMPUESTO_CHOICES, default='Ninguno')
    total_impuesto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valor_impuesto = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def valor_impuesto(self):
        """Calcula el valor del impuesto basado en el porcentaje."""
        if self.impuesto == 'Ninguno':
            return Decimal('0.00')
        elif self.impuesto == 'IVA Exento (0%)':
            return Decimal('0.00')
        elif self.impuesto == 'IVA Excluido (0%)':
            return Decimal('0.00')
        elif self.impuesto == 'IVA (5.00%)':
            return self.total * Decimal('0.05')
        elif self.impuesto == 'IVA (19.00%)':
            return self.total * Decimal('0.19')
        elif self.impuesto == 'IVA (8.00%)':
            return self.total * Decimal('0.08')
        return Decimal('0.00')

    def total_con_impuesto(self):
        """Calcula el total aplicando el impuesto correspondiente."""
        self.valor_impuesto = self.valor_impuesto()
        total = self.total + self.valor_impuesto
        self.total_impuesto = total
        
        return total

    def __str__(self):
        return f"Compra {self.id} - Mesa {self.mesa.numero} - {self.fecha_compra}"

class CompraDetalleDomicilio(models.Model):
    compra = models.ForeignKey('ventas.CompraDomicilio', on_delete=models.CASCADE, related_name='detalles')
    plato = models.ForeignKey('platos.Plato', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return f"Compra {self.compra.id} - Plato: {self.plato.nombre} - Cantidad: {self.cantidad}"