# Generated by Django 4.0.3 on 2022-03-28 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books_api', '0003_order_shippingaddress_review_orderitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]