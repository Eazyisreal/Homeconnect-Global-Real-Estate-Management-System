from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate, logout
from django.views import View
from django.views.generic.edit import FormView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import SignUpForm

class SignUpView(FormView):
    template_name = 'authentication/register.html'
    form_class = SignUpForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        email = form.cleaned_data.get('email')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(email=email, password=raw_password)
        login(self.request, user)
        return super().form_valid(form)

class UserLoginView(FormView):
    template_name = 'authentication/login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        email = self.request.POST.get('username')
        password = self.request.POST.get('password')
        user = authenticate(self.request, email=email, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            messages.error(self.request, "Invalid email or password")
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please provide both email and password")
        return super().form_invalid(form)

class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')

# Password reset views (these are already class-based views)
class CustomPasswordResetView(PasswordResetView):
    template_name = 'authentication/reset_password.html'
    success_url = reverse_lazy('password_reset_done')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'authentication/password_reset_complete.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'authentication/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'authentication/reset_password_complete.html'
