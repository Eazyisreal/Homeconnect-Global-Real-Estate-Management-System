import os
import sys
import csv
from django.core.management.base import BaseCommand
from django.conf import settings
from main.models import Property, Agent, Property_Category

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Homeconnect_Global_Real_Estate_Management_System.settings')

# Import the settings module
import django
django.setup()

class Command(BaseCommand):
    help = 'Import properties from CSV file'

    def handle(self, *args, **options):
        with open('properties.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                property_category, _ = Property_Category.objects.get_or_create(name=row['category'])
                agent, _ = Agent.objects.get_or_create(name=row['associated_agent'])
                property = Property(
                    availability=row['availability'],
                    title=row['title'],
                    location=row['location'],
                    category=property_category,
                    price=row['price'],
                    living_room=row['living_room'],
                    dining=row['dining'],
                    no_of_bedrooms=row['no_of_bedrooms'],
                    no_of_bathrooms=row['no_of_bathrooms'],
                    no_of_floors=row['no_of_floors'],
                    features=row['features'],
                    associated_agent=agent,
                )
                property.save()

if __name__ == '__main__':
    Command().handle()