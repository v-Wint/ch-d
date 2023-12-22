from django import forms
from .models import PrivateEntry

import requests as req
import re

class PrivateEntryForm(forms.ModelForm):
    """Form for private entry creation, moderation etc"""
    class Meta:
        model = PrivateEntry
        exclude = ('added_by', 'number', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

        self.fields['text'].widget.attrs['rows'] = 25
    
    def is_valid(self):
        is_valid = super().is_valid()

        for field in self.fields:
            self[field].field.widget.attrs['class'] = 'form-control is-invalid' if field in self.errors else 'form-control'
        
        return is_valid

    def clean_youtube(self):
        youtube = self.cleaned_data['youtube']

        if req.get(f"https://www.youtube.com/oembed?url={youtube}", timeout=10).status_code == 400:
            raise forms.ValidationError('Invalid youtube link')
        
        return youtube
    
    def clean_spotify(self):
        spotify = self.cleaned_data['spotify']
        if spotify and not re.search(r'^(spotify:|https://[a-z]+\.spotify\.com/)', spotify):
            raise forms.ValidationError('Invalid spotify link')
        
        return spotify
