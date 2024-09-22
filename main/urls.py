from django.urls import path
from .views import *

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about-us', AboutPageView.as_view(), name='about'),
    path('team', TeamPageView.as_view(), name='team'),
    path('contact', ContactPageView.as_view(), name='contact'),
    path('properties', PropertiesPageView.as_view(), name='properties'),
    path('management', ManagementPageView.as_view(), name='management'),
    path('properties_details/',  PropertiesDetailsPageView.as_view(), name='properties_details'), 
    path('management_details/',  ManagementDetailsPageView.as_view(), name='management_details'), 
    
]
