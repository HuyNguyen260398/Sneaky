# Generated by Django 2.2.5 on 2019-09-28 03:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0002_billingprofile_payment_method'),
    ]

    operations = [
        migrations.RenameField(
            model_name='billingprofile',
            old_name='payment_method',
            new_name='payment_option',
        ),
    ]
