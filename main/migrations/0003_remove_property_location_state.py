# Generated by Django 4.2.14 on 2024-09-26 14:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_rename_property_type_property_location_state_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='property',
            name='location_state',
        ),
    ]
