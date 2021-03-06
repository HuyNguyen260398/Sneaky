# Generated by Django 2.2.5 on 2019-09-13 15:37

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='address_line_1',
            new_name='appartment_addresss',
        ),
        migrations.RenameField(
            model_name='address',
            old_name='email',
            new_name='street_address',
        ),
        migrations.RenameField(
            model_name='address',
            old_name='first_name',
            new_name='zip',
        ),
        migrations.RemoveField(
            model_name='address',
            name='address_line_2',
        ),
        migrations.RemoveField(
            model_name='address',
            name='address_type',
        ),
        migrations.RemoveField(
            model_name='address',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='address',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='address',
            name='postal_code',
        ),
        migrations.RemoveField(
            model_name='address',
            name='state',
        ),
        migrations.AlterField(
            model_name='address',
            name='country',
            field=django_countries.fields.CountryField(max_length=2),
        ),
    ]
