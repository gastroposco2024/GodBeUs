from django.db import models
from django.contrib.auth.models import User

class Mesa(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    numero = models.PositiveIntegerField()
    capacidad = models.PositiveIntegerField()
    estado = models.CharField(max_length=10, choices=[('Libre', 'Libre'), ('Ocupada', 'Ocupada')])

    class Meta:
        unique_together = ('numero', 'usuario')

    def __str__(self):
        return f"Mesa {self.numero}"
