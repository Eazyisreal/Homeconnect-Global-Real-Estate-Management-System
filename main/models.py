from django.db import models
from cloudinary.models import CloudinaryField
from django.utils.text import slugify
# from authentication.models import CustomUser


class Management_Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Management Categories'

    def __str__(self):
        return self.name

class Property_Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Property Categories'

    def __str__(self):
        return self.name

class Agent(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=255)
    image = CloudinaryField('image', null=True, blank=True)

    def __str__(self):
        return self.name
    
    

class Management(models.Model):
    AVAILABILITY_CHOICES = [
        ('Selling', 'Selling'),
        ('Rent', 'Rent'),
    ]
    availability = models.CharField(max_length=12, choices=AVAILABILITY_CHOICES)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    details = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    price = models.IntegerField()
    status = models.CharField(max_length=100)
    category = models.ForeignKey(Management_Category, on_delete=models.CASCADE)
    no_of_bedrooms = models.IntegerField()
    no_of_bathrooms = models.IntegerField()
    no_of_floors = models.IntegerField()
    thumbnail = CloudinaryField('image', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    features = models.CharField(max_length=255)
    associated_agent = models.ManyToManyField(Agent)
    slug = models.SlugField(unique=True, max_length=255, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title if self.title else "Untitled Property Listing"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-updated', '-created']
        verbose_name = "Management"
        verbose_name_plural = "Managements"

class Property(models.Model):
    AVAILABILITY_CHOICES = [
        ('Selling', 'Selling'),
        ('Rent', 'Rent'),
    ]
    availability = models.CharField(max_length=12, choices=AVAILABILITY_CHOICES)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    details = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    category = models.ForeignKey(Property_Category, on_delete=models.CASCADE)
    price = models.IntegerField()
    living_room = models.IntegerField()
    dining = models.IntegerField()
    no_of_bedrooms = models.IntegerField()
    no_of_bathrooms = models.IntegerField()
    no_of_floors = models.IntegerField()
    thumbnail = CloudinaryField('image', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    features = models.CharField(max_length=255)
    associated_agent = models.ManyToManyField(Agent)
    slug = models.SlugField(unique=True, max_length=255, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title if self.title else "Untitled Property Listing"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-updated', '-created']
        verbose_name = "Property"
        verbose_name_plural = "Properties"

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    associated_property_image = CloudinaryField('image', null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class ManagementImage(models.Model):
    Management = models.ForeignKey(Management, on_delete=models.CASCADE)
    associated_Management_image = CloudinaryField('image', null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15, blank=True, null=True)  
    location = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f" Contact Message from {self.name} - {self.email}"
    

class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email

class PropertyContactMessage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='property_messages')
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, blank=True, null=True)  
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inspection Booking for {self.property}"


class ManagementContactMessage(models.Model):
    managed_property = models.ForeignKey(Management, on_delete=models.CASCADE, related_name='managed_property_messages')
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, blank=True, null=True)  
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Contact Message about {self.managed_property}"