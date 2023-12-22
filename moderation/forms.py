from django import forms
from public.models import Comment


class CommentForm(forms.ModelForm):
    """For used for comment moderation"""
    body = forms.CharField(widget=forms.Textarea())
    class Meta:
        model = Comment
        exclude = ('is_moderated', )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.disabled = True
