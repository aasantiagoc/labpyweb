# Generated by Django 5.2.3 on 2025-06-13 02:52

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venta', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id_producto', models.AutoField(primary_key=True, serialize=False)),
                ('nom_prod', models.CharField(error_messages={'max_length': 'El texto debe tener un máximo de 50 caracteres'}, max_length=50)),
                ('des_prod', models.CharField(error_messages={'max_length': 'El texto debe tener un máximo de 500 caracteres'}, max_length=500)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0.01)])),
                ('stock', models.PositiveIntegerField(default=0)),
                ('activo', models.BooleanField(default=True)),
                ('fec_vencim', models.DateField()),
                ('fecha_reg', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
