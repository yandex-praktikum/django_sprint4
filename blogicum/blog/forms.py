from django import forms

from django.forms import ModelForm
from .models import Comment, Location, Post, User


class CommentForm(ModelForm):
    model=Comment
    fields=('text',)
    witgets={
# поля для ввода коментария
        'text': forms.Textarea({'rows': '4', 'cols': '50'})
    }