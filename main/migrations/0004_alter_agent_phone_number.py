# Generated by Django 4.2.14 on 2024-09-26 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_remove_property_location_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agent',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
