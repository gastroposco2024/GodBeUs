# Generated by Django 5.0.7 on 2024-07-21 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_alter_profile_address_alter_profile_company_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='apellidos',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='correo',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='direccion',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='municipio_departamento',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='nombre',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='numero_identificacion',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='responsabilidad_tributaria',
            field=models.CharField(blank=True, choices=[('Responsable del IVA', 'Responsable del IVA'), ('No - Impuesto Nacional al Consumo - INC', 'No - Impuesto Nacional al Consumo - INC'), ('No resp de INC', 'No resp de INC'), ('Resp de IVA e INC', 'Resp de IVA e INC'), ('Régimen especial', 'Régimen especial')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='segundo_nombre',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='tipo_documento',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='tipo_persona',
            field=models.CharField(blank=True, choices=[('Nacional', 'Nacional'), ('Extranjero', 'Extranjero')], max_length=20, null=True),
        ),
    ]
