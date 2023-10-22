from typing import Any
from django.db import models
from django.shortcuts import get_object_or_404, render
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)

from .models import Post, Category, User
from .forms import CommentForm, UserForm, PostForm

POST_ID = 'post_id'
POSTS_LIMIT = 5


# Главная страница
class IndexView(ListView):
    paginate_by=POSTS_LIMIT
    template_name = 'blog/index.html'
# IndexView is missing a QuerySet. Define IndexView.model, IndexView.queryset, or override IndexView.get_queryset()
    queryset=Post.post_objects.select_related()

# Страница постов
#def post_detail(request, id):
#    template = 'blog/detail.html'
#    post = get_object_or_404(
#        Post.post_objects,
#        pk=id
#    )
#    context = {'post': post}
#    return render(request, template, context)
class PostDetailView(DetailView):
    model=Post
    pk_url_kwarg = POST_ID
    form_class=CommentForm
    template_name = 'blog/detail.html'

# Reverse for 'create_post' not found. 'create_post' is not a valid view function or pattern name
class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'


def category_posts(request, category_slug):
    '''
    Страница категорий
    '''
    template = 'blog/category.html'
    category = get_object_or_404(Category,
                                 slug=category_slug,
                                 is_published=True,
                                 )
    category_posts = Post.post_objects.filter(category=category)
    context = {'category': category, 'post_list': category_posts}
    return render(request, template, context)


# The current path, accounts/profile/, didn’t match any of these
class ProfileDetailView(DetailView):
    model=User
    form_class=UserForm
    template_name='blog/profile.html'
    slug_url_kwarg = 'username'
    slug_field = 'username'
    context_object_name = 'profile'
 

# Reverse for 'profile' not found. 'profile' is not a valid view function or pattern name
class ProfileUpdateView(UpdateView):
    model=User
    form_class=UserForm
    template_name='blog/user.html'

    def get_object(self):
        return self.request.user
