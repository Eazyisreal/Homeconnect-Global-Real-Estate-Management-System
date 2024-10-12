from django.views.generic import TemplateView, ListView,  DetailView, FormView
from django.db.models import Max, Count
from django.shortcuts import get_object_or_404
from .models import *
from main.forms import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic.edit import FormMixin
from django.views.generic import ListView
from django.db.models import Q




def handle_email_subscription(request, form_data):
    form = NewsletterSubscriptionForm(form_data)
    if form.is_valid():
        email = form.cleaned_data['email']
        if NewsletterSubscription.objects.filter(email=email).exists():
            return 'You are already subscribed.'
        else:
            subscription = NewsletterSubscription(email=email)
            subscription.save()
            return 'Your subscription has been successful!'
    else:
        return None
    
    



def paginate_items(request, items, items_per_page):
    """
    Paginates a list of items based on the request and number of items per page.

    Args:
    - request: Django HttpRequest object.
    - items: QuerySet or list of items to paginate.
    - items_per_page: Number of items to display per page.

    Returns:
    - Paginated items (Page object).
    """
    paginator = Paginator(items, items_per_page)
    page_number = request.GET.get('page')

    try:
        paginated_items = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_items = paginator.page(1)
    except EmptyPage:
        paginated_items = paginator.page(paginator.num_pages)
    return paginated_items





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
                    {'title': 'Contact Us', 'url': '/contact'},
                ]
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



    
    
    
class HomePageView(QuickLinksMixin, TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        properties = Property.objects.all().order_by('created')[:6]
        managed_properties = Management.objects.all().order_by('created')[:6]
        locations = Property.objects.values_list('location', flat=True).distinct()
        categories = Property_Category.objects.values_list('name', flat=True).distinct()
        listing_types = ['Rent', 'Selling']  
        context['properties'] = properties
        context['managed_properties'] = managed_properties
        context['locations'] = locations
        context['categories'] = categories
        context['listing_types'] = listing_types
        return context


class AboutPageView(QuickLinksMixin, TemplateView):
    template_name = 'about.html'


class TeamPageView(QuickLinksMixin, TemplateView):
    template_name = 'team.html'


class ContactView(QuickLinksMixin, FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['newsletter_form'] = NewsletterSubscriptionForm()
        context['contact_form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        if 'newsletter_form' in request.POST:
            newsletter_form = NewsletterSubscriptionForm(request.POST)
            if newsletter_form.is_valid():
                handle_email_subscription(request, newsletter_form, 'contact')
                messages.success(
                    request, 'You have successfully subscribed to the newsletter!')
        else:
            contact_form = self.get_form()
            if contact_form.is_valid():
                return self.form_valid(contact_form)
        return self.form_invalid(self.get_form())

    def form_valid(self, form):
        contact_message = ContactMessage.objects.create(
            name=form.cleaned_data['name'],
            email=form.cleaned_data['email'],
            phone_number=form.cleaned_data['phone_number'],
            location=form.cleaned_data['location'],
            message=form.cleaned_data['message']
        )
        contact_message.save()
        messages.success(
            self.request, 'Your message has been sent successfully! We will get back to you soon.')
        return super().form_valid(form)


class ManagementListView(QuickLinksMixin, ListView):
    template_name = 'management.html'
    model = Management
    context_object_name = 'properties'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Management_Category.objects.all()
        properties = Management.objects.all().order_by('-id')
        paginated_properties = paginate_items(
            self.request, properties, items_per_page=6)
        context['properties'] = properties
        context['categories'] = categories
        context['selected_category'] = self.kwargs.get('category_name')
        context['paginated_properties'] = paginated_properties

        return context


class ManagementDetailView(QuickLinksMixin, FormMixin, DetailView):
    template_name = 'management_details.html'
    model = Management
    context_object_name = 'property'
    slug_field = 'slug'
    slug_url_kwarg = 'property_slug'
    form_class = ManagementContactForm
    success_url = reverse_lazy('management_details')
    
    
    def get_success_url(self):
        return reverse_lazy('management_details', kwargs={'property_slug': self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        available_properties = Management.objects.all().order_by('-id')
        paginated_properties = paginate_items(self.request, available_properties, items_per_page=6)
        property_instance = self.get_object()
        images = property_instance.managementimage_set.all()
        agents = property_instance.associated_agent.all()
        features_list = property_instance.features.split(',')
        context.update({
            'available_properties': available_properties,
            'images': images,
            'agents': agents,
            'paginated_properties': paginated_properties,
            'features_list': [feature.strip() for feature in features_list],
            'property_form': self.get_form(),
        })
        return context
    
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'newsletter_form' in request.POST:
            newsletter_form = NewsletterSubscriptionForm(request.POST)
            if newsletter_form.is_valid():
                handle_email_subscription(request, newsletter_form, 'contact')
                messages.success(request, 'You have successfully subscribed to the newsletter!')
            return self.get(request, *args, **kwargs)
        else:
            form = self.get_form()
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)

    def form_valid(self, form):
        property_instance = self.get_object()
        contact_message = ManagementContactMessage.objects.create(
            managed_property=property_instance,
            name=form.cleaned_data['name'],
            email=form.cleaned_data['email'],
            phone_number=form.cleaned_data['phone_number'],
            message=form.cleaned_data['message']
        )
        contact_message.save()
        messages.success(self.request, 'Your message has been sent successfully! We will get back to you soon.')
        return super().form_valid(form)





class PropertyListView(QuickLinksMixin, ListView):
    template_name = 'properties.html'
    model = Property
    context_object_name = 'properties'

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Category filter
        category_name = self.kwargs.get('category_name')
        if category_name:
            category_obj = get_object_or_404(Property_Category, name=category_name)
            queryset = queryset.filter(category=category_obj)
        
     
        
        filters = Q()
        
        keyword = self.request.GET.get('keyword')
        if keyword:
            filters |= Q(title__icontains=keyword) | Q(description__icontains=keyword)
        
        location = self.request.GET.get('location')
        if location:
            filters &= Q(location__icontains=location)
        
        property_type = self.request.GET.get('property_type')
        if property_type:
            filters &= Q(category__name=property_type)
        
        listing_type = self.request.GET.get('listing_type')
        if listing_type:
            filters &= Q(availability=listing_type)
        
        for param in ['bedrooms', 'bathrooms', 'floor']:
            value = self.request.GET.get(param)
            if value:
                filters &= Q(**{f'no_of_{param}': value})
        
        return queryset.filter(filters)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        properties = Property.objects.all()
        locations = Property.objects.values_list('location', flat=True).distinct()
        categories = Property_Category.objects.values_list('name', flat=True).distinct()
        listing_types = ['Rent', 'Selling']  
        context['locations'] = locations
        context['categories'] = categories
        context['listing_types'] = listing_types
        # Quick filter options
        context['bedroom_options'] = properties.values('no_of_bedrooms').annotate(count=Count('no_of_bedrooms')).order_by('no_of_bedrooms')
        context['bathroom_options'] = properties.values('no_of_bathrooms').annotate(count=Count('no_of_bathrooms')).order_by('no_of_bathrooms')
        context['floor_options'] = properties.values('no_of_floors').annotate(count=Count('no_of_floors')).order_by('no_of_floors')

        # Max values for range inputs
        context['max_bedrooms'] = properties.aggregate(Max('no_of_bedrooms'))['no_of_bedrooms__max']
        context['max_bathrooms'] = properties.aggregate(Max('no_of_bathrooms'))['no_of_bathrooms__max']
        context['max_floors'] = properties.aggregate(Max('no_of_floors'))['no_of_floors__max']

        # Other context data
        context['categories'] = Property_Category.objects.all()
        context['selected_category'] = self.kwargs.get('category_name')
        context['paginated_properties'] = paginate_items(self.request, self.get_queryset(), items_per_page=6)

        return context




class PropertyDetailView(QuickLinksMixin, FormMixin, DetailView):
    model = Property
    template_name = 'properties_details.html'
    context_object_name = 'property'
    slug_field = 'slug'
    slug_url_kwarg = 'property_slug'
    form_class = PropertyContactForm
    success_url = reverse_lazy('properties_details')

    def get_success_url(self):
        return reverse_lazy('properties_details', kwargs={'property_slug': self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        available_properties = Property.objects.all().order_by('-id')
        paginated_properties = paginate_items(self.request, available_properties, items_per_page=6)
        property_instance = self.get_object()
        images = property_instance.propertyimage_set.all()
        agents = property_instance.associated_agent.all()
        features_list = property_instance.features.split(',')
        context.update({
            'available_properties': available_properties,
            'images': images,
            'agents': agents,
            'paginated_properties': paginated_properties,
            'features_list': [feature.strip() for feature in features_list],
            'property_form': self.get_form(),
        })
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'newsletter_form' in request.POST:
            newsletter_form = NewsletterSubscriptionForm(request.POST)
            if newsletter_form.is_valid():
                handle_email_subscription(request, newsletter_form, 'contact')
                messages.success(request, 'You have successfully subscribed to the newsletter!')
            return self.get(request, *args, **kwargs)
        else:
            form = self.get_form()
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)

    def form_valid(self, form):
        property_instance = self.get_object()
        contact_message = PropertyContactMessage.objects.create(
            property=property_instance,
            name=form.cleaned_data['name'],
            email=form.cleaned_data['email'],
            phone_number=form.cleaned_data['phone_number'],
            message=form.cleaned_data['message']
        )
        contact_message.save()
        messages.success(self.request, 'Your message has been sent successfully! We will get back to you soon.')
        return super().form_valid(form)