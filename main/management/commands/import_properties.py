import csv
from django.core.management import BaseCommand
from main.models import Property, Agent, Property_Category, PropertyImage, Management, Management_Category, ManagementImage

class Command(BaseCommand):
    help = 'Populate database models from CSV file'

    def handle(self, *args, **options):
        # Populate Property model
        with open('properties.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row

            # Create Property Categories
            property_categories = {}
            for row in reader:
                category_name = row[3]
                if category_name not in property_categories:
                    category = Property_Category(name=category_name)
                    category.save()
                    property_categories[category_name] = category

            # Create Agents
            agents = {}
            for row in reader:
                agent_name = row[11]
                if agent_name not in agents:
                    agent = Agent(name=agent_name)
                    agent.save()
                    agents[agent_name] = agent

            # Create Properties
            for row in reader:
                availability = row[0]
                title = row[1]
                location = row[2]
                category_name = row[3]
                price = int(row[4])
                living_room = int(row[5])
                dining = int(row[6])
                no_of_bedrooms = int(row[7])
                no_of_bathrooms = int(row[8])
                no_of_floors = int (row[9])
                features = row[10]
                associated_agent_name = row[11]

                category = property_categories[category_name]
                associated_agent = agents[associated_agent_name]

                property = Property(
                    availability=availability,
                    title=title,
                    location=location,
                    category=category,
                    price=price,
                    living_room=living_room,
                    dining=dining,
                    no_of_bedrooms=no_of_bedrooms,
                    no_of_bathrooms=no_of_bathrooms,
                    no_of_floors=no_of_floors,
                    features=features,
                )
                property.save()
                property.associated_agent.add(associated_agent)

                # Create Property Images
                property_image = PropertyImage(property=property)
                property_image.save()

        # Populate Management model
        with open('managements.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row

            # Create Management Categories
            management_categories = {}
            for row in reader:
                category_name = row[2]
                if category_name not in management_categories:
                    category = Management_Category(name=category_name)
                    category.save()
                    management_categories[category_name] = category

            # Create Managements
            for row in reader:
                title = row[0]
                location = row[1]
                category_name = row[2]
                price = int(row[3])
                status = row[4]
                no_of_block = int(row[5])
                no_of_flat = int(row[6])
                no_of_floors = int(row[7])

                category = management_categories[category_name]

                management = Management(
                    title=title,
                    location=location,
                    category=category,
                    price=price,
                    status=status,
                    no_of_block=no_of_block,
                    no_of_flat=no_of_flat,
                    no_of_floors=no_of_floors,
                )
                management.save()

                # Create Management Images
                management_image = ManagementImage(Management=management)
                management_image.save()

        self.stdout.write(self.style.SUCCESS('Successfully populated database models'))