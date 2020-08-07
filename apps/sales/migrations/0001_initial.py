# Generated by Django 3.0.8 on 2020-07-19 13:42

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('entries', '0007_auto_20200713_0654'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('state', models.BooleanField(default=True, verbose_name='State')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(auto_now=True)),
                ('type_receipt', models.CharField(max_length=50)),
                ('num_receipt', models.CharField(max_length=50)),
                ('serie_receipt', models.CharField(max_length=50)),
                ('tax', models.DecimalField(decimal_places=2, max_digits=4)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entries.Person')),
            ],
            options={
                'verbose_name': 'Sale',
                'verbose_name_plural': 'Sales',
            },
        ),
        migrations.CreateModel(
            name='SaleDetail',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('state', models.BooleanField(default=True, verbose_name='State')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(auto_now=True)),
                ('quantity', models.IntegerField()),
                ('sale_price', models.DecimalField(decimal_places=2, max_digits=11)),
                ('discount', models.DecimalField(decimal_places=2, max_digits=11)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entries.Item')),
                ('sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.Sale')),
            ],
            options={
                'verbose_name': 'EntryDetail',
                'verbose_name_plural': 'EntriesDetail',
            },
        ),
    ]