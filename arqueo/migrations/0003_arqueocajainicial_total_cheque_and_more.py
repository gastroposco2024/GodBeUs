# Generated by Django 5.0.7 on 2024-07-21 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arqueo', '0002_arqueocajainicial_estado'),
    ]

    operations = [
        migrations.AddField(
            model_name='arqueocajainicial',
            name='total_cheque',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='arqueocajainicial',
            name='total_consignacion',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='arqueocajainicial',
            name='total_efectivo',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='arqueocajainicial',
            name='total_tarjeta_credito',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='arqueocajainicial',
            name='total_tarjeta_debito',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='arqueocajainicial',
            name='total_transferencia',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
