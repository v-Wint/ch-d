from django.contrib.auth.forms import UserChangeForm
from accounts.models import User
from django import forms

class UpdateUserForm(UserChangeForm):
    """Form for editing user information"""
    class Meta:
        model = User
        fields = ['username', 'email', 'about', 'pfp']

        widgets = {
            'about': forms.Textarea()
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
    
    def is_valid(self):
        is_valid = super().is_valid()

        for field in self.fields:
            self[field].field.widget.attrs['class'] = 'form-control is-invalid' if field in self.errors else 'form-control is-valid'
        
        return is_valid
