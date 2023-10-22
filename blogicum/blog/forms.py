from django import forms

from django.forms import ModelForm
from .models import Comment, Location, Post, User


class CommentForm(ModelForm):
    model=Comment
    fields=('text',)
    witgets={
# Поле для ввода коментария
        'text': forms.Textarea({'rows': '4', 'cols': '50'})
    }

# Reverse for 'profile' not found. 'profile' is not a valid view function or pattern name
class UserForm(ModelForm):

    class Meta:
        model=User
        fields=(
            'username',
            'first_name',
            'last_name',
            'email'
        )

# Reverse for 'create_post' not found. 'create_post' is not a valid view function or pattern name
class PostForm(ModelForm):

    class Meta:
        model = Post
        exclude = ('author',)
# Виджет для даты публикации
        widgets = {
            'pub_date': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control'
                },
                format=('%Y-%m-%d %H:%M:%S')
            )
        }