# Generated by Django 3.0.8 on 2020-07-13 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entries', '0003_auto_20200713_0357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='gramsOrMilliliters',
            field=models.DecimalField(decimal_places=2, default=None, max_digits=6),
        ),
    ]
