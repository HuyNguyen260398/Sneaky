# Generated by Django 2.2.5 on 2019-09-14 00:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0002_auto_20190913_2237'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='address_type',
            field=models.CharField(choices=[('billing', 'Billing'), ('shipping', 'Shipping')], default=django.utils.timezone.now, max_length=120),
            preserve_default=False,
        ),
    ]
