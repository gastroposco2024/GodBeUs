from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal

class ArqueoCajaInicial(models.Model):
    ESTADO_EN_CURSO = 'En Curso'
    ESTADO_FINALIZADO = 'Finalizado'
    ESTADOS = [
        (ESTADO_EN_CURSO, 'En Curso'),
        (ESTADO_FINALIZADO, 'Finalizado'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_inicio = models.DateTimeField(default=timezone.now)
    fecha_fin = models.DateTimeField(null=True, blank=True)
    efectivo_inicial = models.DecimalField(max_digits=10, decimal_places=2)
    efectivo_final = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    efectivo_final_registrado = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_ventas = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_ventas_domicilios = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_pagos = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    diferencias = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    observaciones = models.TextField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default=ESTADO_EN_CURSO)

    # Campos para conteo de monedas y billetes
    monedas_50 = models.IntegerField(default=0)
    monedas_100 = models.IntegerField(default=0)
    monedas_200 = models.IntegerField(default=0)
    monedas_500 = models.IntegerField(default=0)
    monedas_1000 = models.IntegerField(default=0)
    billetes_2000 = models.IntegerField(default=0)
    billetes_5000 = models.IntegerField(default=0)
    billetes_10000 = models.IntegerField(default=0)
    billetes_20000 = models.IntegerField(default=0)
    billetes_50000 = models.IntegerField(default=0)
    billetes_100000 = models.IntegerField(default=0)

    # Campos para los métodos de pago
    total_efectivo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_consignacion = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_transferencia = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_cheque = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_tarjeta_credito = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_tarjeta_debito = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    total_efectivo_domicilios = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_consignacion_domicilios = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_transferencia_domicilios = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_cheque_domicilios = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_tarjeta_credito_domicilios = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_tarjeta_debito_domicilios = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    

    def calcular_total_efectivo(self):
        total_monedas = (
            self.monedas_50 * 50 +
            self.monedas_100 * 100 +
            self.monedas_200 * 200 +
            self.monedas_500 * 500 +
            self.monedas_1000 * 1000
        )
        total_billetes = (
            self.billetes_2000 * 2000 +
            self.billetes_5000 * 5000 +
            self.billetes_10000 * 10000 +
            self.billetes_20000 * 20000 +
            self.billetes_50000 * 50000 + 
            self.billetes_100000 * 100000
        )

        self.efectivo_final_registrado = total_monedas + total_billetes

    def calcular_totales(self):
        from ventas.models import Compra, CompraDomicilio
        from pagos.models import Pago

        # Filtrar ventas y pagos por usuario y por rango de fechas
        ventas = Compra.objects.filter(usuario=self.usuario, fecha_compra__range=[self.fecha_inicio, self.fecha_fin])
        ventas_domicilios = CompraDomicilio.objects.filter(usuario=self.usuario, fecha_compra__range=[self.fecha_inicio, self.fecha_fin])
        pagos = Pago.objects.filter(usuario=self.usuario, fecha__range=[self.fecha_inicio, self.fecha_fin])
        

        # Calcular el total de ventas y pagos
        self.total_ventas = ventas.aggregate(models.Sum('total'))['total__sum'] or Decimal('0.00')
        self.total_ventas_domicilios = ventas_domicilios.aggregate(models.Sum('total'))['total__sum'] or Decimal('0.00')
        self.total_pagos = pagos.aggregate(models.Sum('valor'))['valor__sum'] or Decimal('0.00')

        

        # Calcular totales por método de pago
        self.total_efectivo = ventas.filter(tipo_pago='Efectivo').aggregate(models.Sum('total'))['total__sum'] or Decimal('0.00')
        self.total_consignacion = ventas.filter(tipo_pago='Consignación').aggregate(models.Sum('total'))['total__sum'] or Decimal('0.00')
        self.total_transferencia = ventas.filter(tipo_pago='Transferencia').aggregate(models.Sum('total'))['total__sum'] or Decimal('0.00')
        self.total_cheque = ventas.filter(tipo_pago='Cheque').aggregate(models.Sum('total'))['total__sum'] or Decimal('0.00')
        self.total_tarjeta_credito = ventas.filter(tipo_pago='Tarjeta crédito').aggregate(models.Sum('total'))['total__sum'] or Decimal('0.00')
        self.total_tarjeta_debito = ventas.filter(tipo_pago='Tarjeta débito').aggregate(models.Sum('total'))['total__sum'] or Decimal('0.00')
        
        # Calcular totales por método de pago
        self.total_efectivo_domicilios = ventas_domicilios.filter(tipo_pago='Efectivo').aggregate(models.Sum('total'))['total__sum'] or Decimal('0.00')
        self.total_consignacion_domicilios = ventas_domicilios.filter(tipo_pago='Consignación').aggregate(models.Sum('total'))['total__sum'] or Decimal('0.00')
        self.total_transferencia_domicilios = ventas_domicilios.filter(tipo_pago='Transferencia').aggregate(models.Sum('total'))['total__sum'] or Decimal('0.00')
        self.total_cheque_domicilios = ventas_domicilios.filter(tipo_pago='Cheque').aggregate(models.Sum('total'))['total__sum'] or Decimal('0.00')
        self.total_tarjeta_credito_domicilios = ventas_domicilios.filter(tipo_pago='Tarjeta crédito').aggregate(models.Sum('total'))['total__sum'] or Decimal('0.00')
        self.total_tarjeta_debito_domicilios = ventas_domicilios.filter(tipo_pago='Tarjeta débito').aggregate(models.Sum('total'))['total__sum'] or Decimal('0.00')

        deducibles = self.total_consignacion + self.total_transferencia + self.total_cheque + self.total_tarjeta_debito + self.total_tarjeta_credito + self.total_pagos
        deducibles_domcilio = self.total_consignacion_domicilios + self.total_transferencia_domicilios + self.total_cheque_domicilios + self.total_tarjeta_debito_domicilios + self.total_tarjeta_credito_domicilios

        # Calcular el efectivo final y las diferencias
        self.efectivo_final = self.efectivo_inicial + self.total_ventas + self.total_ventas_domicilios - (deducibles + deducibles_domcilio)
        self.diferencias = self.efectivo_final - self.efectivo_inicial

        self.save()

    def calcular_totales_domicilios(self):
        from ventas.models import CompraDomicilio

        # Filtrar ventas y pagos por usuario y por rango de fechas
        ventas = CompraDomicilio.objects.filter(usuario=self.usuario, fecha_compra__range=[self.fecha_inicio, self.fecha_fin])

        # Calcular el total de ventas y pagos
        self.total_ventas = ventas.aggregate(models.Sum('total'))['total__sum'] or Decimal('0.00')

        # Calcular el efectivo final y las diferencias
        self.efectivo_final = self.efectivo_inicial + self.total_ventas - self.total_pagos
        self.diferencias = self.efectivo_final - self.efectivo_inicial

        # Calcular totales por método de pago
        self.total_efectivo = ventas.filter(tipo_pago='Efectivo').aggregate(models.Sum('total'))['total__sum'] or Decimal('0.00')
        self.total_consignacion = ventas.filter(tipo_pago='Consignación').aggregate(models.Sum('total'))['total__sum'] or Decimal('0.00')
        self.total_transferencia = ventas.filter(tipo_pago='Transferencia').aggregate(models.Sum('total'))['total__sum'] or Decimal('0.00')
        self.total_cheque = ventas.filter(tipo_pago='Cheque').aggregate(models.Sum('total'))['total__sum'] or Decimal('0.00')
        self.total_tarjeta_credito = ventas.filter(tipo_pago='Tarjeta crédito').aggregate(models.Sum('total'))['total__sum'] or Decimal('0.00')
        self.total_tarjeta_debito = ventas.filter(tipo_pago='Tarjeta débito').aggregate(models.Sum('total'))['total__sum'] or Decimal('0.00')
        
        self.save()

    def ventas_por_metodo_pago(self):
        """Devuelve un diccionario con el total de ventas por método de pago."""
        from ventas.models import Compra

        ventas = Compra.objects.filter(usuario=self.usuario, fecha_compra__range=[self.fecha_inicio, self.fecha_fin])
        resultados = ventas.values('tipo_pago').annotate(total_ventas=models.Sum('total'))

        return {resultado['tipo_pago']: resultado['total_ventas'] for resultado in resultados}

    def ventas_por_metodo_pago_domicilios(self):
        """Devuelve un diccionario con el total de ventas por método de pago."""
        from ventas.models import CompraDomicilio

        ventas_domicilios = CompraDomicilio.objects.filter(usuario=self.usuario, fecha_compra__range=[self.fecha_inicio, self.fecha_fin])
        resultados_domicilios = ventas_domicilios.values('tipo_pago').annotate(total_ventas=models.Sum('total'))

        return {resultado['tipo_pago']: resultado['total_ventas'] for resultado in resultados_domicilios}

    def pagos_por_metodo_pago(self):
        """Devuelve un diccionario con el total de pagos por método de pago."""
        from pagos.models import Pago

        pagos = Pago.objects.filter(usuario=self.usuario, fecha__range=[self.fecha_inicio, self.fecha_fin])
        resultados = pagos.values('metodo_pago').annotate(total_pagos=models.Sum('valor'))
        return {resultado['metodo_pago']: resultado['total_pagos'] for resultado in resultados}

    def __str__(self):
        return f"Arqueo de Caja - {self.usuario.username} - {self.fecha_inicio}"
