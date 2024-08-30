from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    RESPONSABILIDAD_TRIBUTARIA_CHOICES = [
        ('Responsable del IVA', 'Responsable del IVA'),
        ('No - Impuesto Nacional al Consumo - INC', 'No - Impuesto Nacional al Consumo - INC'),
        ('No resp de INC', 'No resp de INC'),
        ('Resp de IVA e INC', 'Resp de IVA e INC'),
        ('Régimen especial', 'Régimen especial'),
    ]
    TIPO_PERSONA_CHOICES = [
        ('Nacional', 'Nacional'),
        ('Extranjero', 'Extranjero'),
    ]
    TIPO_DOCUMENTO_CHOICES = [
        ('CC', 'Cédula de Ciudadanía'),
        ('NIT', 'NIT'),
        ('Pasaporte', 'Pasaporte'),
        ('TI', 'Tarjeta de Identidad'),
        ('CE', 'Cédula de Extranjería'),
        ('RUC', 'RUC'),
        ('Otro', 'Otro'),
    ]

    # Datos Usuario
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)

    # Datos Empresa
    tipo_documento = models.CharField(
        max_length=20,
        choices=TIPO_DOCUMENTO_CHOICES,
        blank=True,
        null=True
    )
    numero_identificacion = models.CharField(max_length=20, blank=True, null=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    segundo_nombre = models.CharField(max_length=100, blank=True, null=True)
    apellidos = models.CharField(max_length=100, blank=True, null=True)
    correo = models.EmailField(blank=True, null=True)
    municipio_departamento = models.CharField(max_length=100, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    
    responsabilidad_tributaria = models.CharField(
        max_length=50,
        choices=RESPONSABILIDAD_TRIBUTARIA_CHOICES,
        blank=True,
        null=True
    )

    tipo_persona = models.CharField(
        max_length=20,
        choices=TIPO_PERSONA_CHOICES,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.user.username

class Cliente(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    direccion = models.CharField(max_length=255)
    documento = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.nombre} - {self.documento}'