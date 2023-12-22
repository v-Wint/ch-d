from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomPasswordChangeForm


class SignUpView(CreateView):
    """View for sign up page"""
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class CustomLoginView(LoginView):
    """View for log in page"""
    authentication_form = CustomAuthenticationForm


class CustomPasswordChangeView(PasswordChangeView):
    """View for password change page"""
    form_class = CustomPasswordChangeForm
