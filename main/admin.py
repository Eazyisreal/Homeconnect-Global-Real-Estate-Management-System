from django.contrib import admin
from .models import *


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1

class PropertyAdmin(admin.ModelAdmin):
    inlines = [PropertyImageInline]
    list_display = ('title', 'price',  'location')
    search_fields = ('title', 'associated_agent__name') 

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'details', 'thumbnail', 'price', 'category', 'location', 'address', 'availability')
        }),
        ('Additional Information', {
            'fields': ('living_room', 'dining' ,'no_of_bedrooms', 'no_of_bathrooms', 'no_of_floors', 'features', 'associated_agent', 'slug')
        }),
    )
    
    prepopulated_fields = {'slug': ('title',)} 
    
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = [ 'associated_property_image']

class ManagementImageInline(admin.TabularInline):
    model = ManagementImage
    extra = 1


class ManagementAdmin(admin.ModelAdmin):
    inlines = [ManagementImageInline]
    list_display = ('title', 'price',  'location')
    search_fields = ('title', 'status') 

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description',  'details', 'thumbnail', 'price', 'category', 'status', 'location', 'address', 'availability')
        }),
        ('Additional Information', {
            'fields': ('no_of_bedrooms', 'no_of_bathrooms', 'no_of_floors', 'features', 'associated_agent', 'slug')
        }),
    )
    
    prepopulated_fields = {'slug': ('title',)} 
    
class ManagementImageAdmin(admin.ModelAdmin):
    list_display = [ 'associated_Management_image']

admin.site.register(Management_Category)
admin.site.register(Management, ManagementAdmin)
admin.site.register(Property_Category)
admin.site.register(PropertyImage, PropertyImageAdmin)
admin.site.register(ManagementImage, ManagementImageAdmin)
admin.site.register(Property, PropertyAdmin)
admin.site.register(Agent)
admin.site.register(ContactMessage)
admin.site.register(NewsletterSubscription)
admin.site.register(PropertyContactMessage)
admin.site.register(ManagementContactMessage)