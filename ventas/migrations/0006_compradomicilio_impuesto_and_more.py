# Generated by Django 5.0.7 on 2024-08-06 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0005_compra_total_impuesto'),
    ]

    operations = [
        migrations.AddField(
            model_name='compradomicilio',
            name='impuesto',
            field=models.CharField(choices=[('Ninguno', 'Ninguno'), ('IVA Exento (0%)', 'IVA Exento (0%)'), ('IVA Excluido (0%)', 'IVA Excluido (0%)'), ('IVA (5.00%)', 'IVA (5.00%)'), ('IVA (19.00%)', 'IVA (19.00%)'), ('IVA (8.00%)', 'IVA (8.00%)')], default='Ninguno', max_length=20),
        ),
        migrations.AddField(
            model_name='compradomicilio',
            name='total_impuesto',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
