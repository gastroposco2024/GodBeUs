# Generated by Django 5.0.7 on 2024-07-29 04:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0002_pedidodomicilio_itempedidodomicilio'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pedidodomicilio',
            name='usuario',
        ),
        migrations.DeleteModel(
            name='ItemPedidoDomicilio',
        ),
        migrations.DeleteModel(
            name='PedidoDomicilio',
        ),
    ]
