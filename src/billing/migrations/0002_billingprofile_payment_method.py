# Generated by Django 2.2.5 on 2019-09-28 03:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='billingprofile',
            name='payment_method',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]