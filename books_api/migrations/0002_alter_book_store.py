# Generated by Django 4.0.3 on 2022-03-28 14:12

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='store',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=200, null=True), size=None),
        ),
    ]
