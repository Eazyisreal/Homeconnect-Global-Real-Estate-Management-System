from django.shortcuts import render
from django.views.generic import TemplateView

class QuickLinksMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quick_links'] = [
            {
                'title': 'Pages',
                'children': [
                    {'title': 'About Us', 'url': '/about-us'},
                    {'title': 'Properties', 'url': '/properties'},
                    {'title': 'Management', 'url': '/management'},
                    {'title': 'Contact Us', 'url': '/contact-us'},                ]
            },
            {
                'title': 'Support',
                'children': [
                    {'title': 'FAQ', 'url': '/faq'},
                    {'title': 'Help Center', 'url': '/help'},
                ]
            },
            {
                'title': 'Legals',
                'children': [
                    {'title': 'Terms of Services', 'url': '/terms-of-service'},
                    {'title': 'Privacy Policy', 'url': '/privacy-policy'},
                ]
            },
        ]
        return context



class HomePageView(QuickLinksMixin,TemplateView):
    template_name = 'home.html'
