from django import forms
from .models import *

NIGERIAN_STATES = [
    ('Abia', 'Umuahia'),
    ('Adamawa', 'Yola'),
    ('Akwa Ibom', 'Uyo'),
    ('Anambra', 'Awka'),
    ('Bauchi', 'Bauchi'),
    ('Bayelsa', 'Yenagoa'),
    ('Benue', 'Makurdi'),
    ('Borno', 'Maiduguri'),
    ('Cross River', 'Calabar'),
    ('Delta', 'Asaba'),
    ('Ebonyi', 'Abakaliki'),
    ('Edo', 'Benin City'),
    ('Ekiti', 'Ado-Ekiti'),
    ('Enugu', 'Enugu'),
    ('Gombe', 'Gombe'),
    ('Imo', 'Owerri'),
    ('Jigawa', 'Dutse'),
    ('Kaduna', 'Kaduna'),
    ('Kano', 'Kano'),
    ('Kogi', 'Lokoja'),
    ('Kwara', 'Ilorin'),
    ('Lagos', 'Ikeja'),
    ('Nasarawa', 'Lafia'),
    ('Niger', 'Minna'),
    ('Ogun', 'Abeokuta'),
    ('Ondo', 'Akure'),
    ('Osun', 'Osogbo'),
    ('Oyo', 'Ibadan'),
    ('Plateau', 'Jos'),
    ('Rivers', 'Port Harcourt'),
    ('Sokoto', 'Sokoto'),
    ('Taraba', 'Jalingo'),
    ('Yobe', 'Damaturu'),
    ('Zamfara', 'Gusau'),
]


NIGERIAN_STATES = sorted(NIGERIAN_STATES, key=lambda x: x[0])

class NewsletterSubscriptionForm(forms.Form):
    email = forms.EmailField()


class PropertyContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=15) 
    message = forms.CharField(widget=forms.Textarea)

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=15, required=False) 
    location = forms.ChoiceField(choices=NIGERIAN_STATES, label="Select State")
    message = forms.CharField(widget=forms.Textarea)

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if phone and not phone.isdigit():
            raise forms.ValidationError("Phone number should contain only digits.")
        return phone

class ManagementContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=15, required=False)
    message = forms.CharField(widget=forms.Textarea)


