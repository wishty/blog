from .models import Comment
from django import forms

class Commentform(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
