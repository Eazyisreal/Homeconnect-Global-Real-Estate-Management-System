from django.urls import path
from .views import *

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about-us', AboutPageView.as_view(), name='about'),
    path('team', TeamPageView.as_view(), name='team'),
    path('contact', ContactView.as_view(), name='contact'),
    path('properties', PropertyListView.as_view(), name='properties'),
    path('management', ManagementListView.as_view(), name='management'),
    path('properties/<slug:property_slug>/', PropertyDetailView.as_view(), name='properties_details'),
    path('management/<slug:property_slug>/',  ManagementDetailView.as_view(), name='management_details'), 
    
]
