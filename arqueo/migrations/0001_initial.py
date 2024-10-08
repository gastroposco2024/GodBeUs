# Generated by Django 5.0.7 on 2024-07-21 06:26

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ArqueoCajaInicial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inicio', models.DateTimeField(default=django.utils.timezone.now)),
                ('fecha_fin', models.DateTimeField(blank=True, null=True)),
                ('efectivo_inicial', models.DecimalField(decimal_places=2, max_digits=10)),
                ('efectivo_final', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('total_ventas', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('total_pagos', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('diferencias', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('observaciones', models.TextField(blank=True, null=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
