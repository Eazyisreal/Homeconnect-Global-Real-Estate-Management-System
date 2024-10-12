from main.forms import NewsletterSubscriptionForm
from main.models import NewsletterSubscription

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
