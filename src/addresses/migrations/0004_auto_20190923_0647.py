# Generated by Django 2.2.5 on 2019-09-22 23:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0003_address_address_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='appartment_addresss',
            new_name='appartment_address',
        ),
    ]
