from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    """Sign up form with Bootstrap widgets"""
    class Meta(UserCreationForm):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
    
    def is_valid(self):
        is_valid = super().is_valid()

        for field in self.fields:
            self[field].field.widget.attrs['class'] = 'form-control is-invalid' \
                if field in self.errors or (field == 'password1' and 'password2' in self.errors) \
                    else 'form-control is-valid'

        return is_valid


class CustomAuthenticationForm(AuthenticationForm):
    """Log in form with Bootstrap widgets"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def is_valid(self):
        is_valid = super().is_valid()

        if '__all__' in self.errors:

            for field in self.fields:
                if field != '__all__':
                    self[field].field.widget.attrs['class'] = 'form-control'
        else:
            for field in self.fields:
                self[field].field.widget.attrs['class'] = 'form-control is-invalid' \
                      if field in self.errors else 'form-control is-valid'

        return is_valid


class CustomPasswordChangeForm(PasswordChangeForm):
    "Password change form with Bootstrap widgets"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def is_valid(self):
        is_valid = super().is_valid()

        if '__all__' in self.errors:

            for field in self.fields:
                if field != '__all__':
                    self[field].field.widget.attrs['class'] = 'form-control'
        else:
            for field in self.fields:
                self[field].field.widget.attrs['class'] = 'form-control is-invalid' \
                      if field in self.errors or (field == 'new_password1' and 'new_password2' in self.errors) \
                          else 'form-control is-valid'
        
        return is_valid
