# Generated by Django 2.2.4 on 2019-09-04 03:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_productvariant_slug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productvariant',
            old_name='sku',
            new_name='title',
        ),
    ]
