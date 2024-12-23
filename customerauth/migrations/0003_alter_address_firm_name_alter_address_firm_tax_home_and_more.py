# Generated by Django 5.1.2 on 2024-12-11 21:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("customerauth", "0002_addressmodel_address_address_model"),
    ]

    operations = [
        migrations.AlterField(
            model_name="address",
            name="firm_name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="address",
            name="firm_tax_home",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="address",
            name="firm_taxcode",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
