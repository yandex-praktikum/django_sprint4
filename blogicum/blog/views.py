from typing import Any
from django.db import models
# Подключите к проекту пагинацию
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from django.urls import reverse_lazy

from .models import Post, Category, User, Comment
from .forms import CommentForm, UserForm, PostForm

POST_ID = 'post_id'
# Настройте вывод не более 10 публикаций
POSTS_LIMIT = 10


# Главная страница
class IndexView(ListView):
# Настройте вывод не более 10 публикаций на главную страницу,
    paginate_by=POSTS_LIMIT
    template_name = 'blog/index.html'
# IndexView is missing a QuerySet. Define IndexView.model, IndexView.queryset, or override IndexView.get_queryset()
    queryset=Post.post_objects.select_related()


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


class PostDeleteView(DeleteView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    pk_url_kwarg = POST_ID


    def get_context_data(self, **kwargs):
        '''Вывод текста поста'''
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm(instance=self.object)
        return context
    

class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    pk_url_kwarg = POST_ID


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
# No URL to redirect to.  Either provide a url or define a get_absolute_url method on the Model  
    def get_success_url(self):
        username = self.request.user.username
        return reverse_lazy('blog:profile', kwargs={'username': username})


class CategoryPostListView(ListView):
    paginate_by = POSTS_LIMIT
    template_name = 'blog/category.html'


class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(
            Post.post_objects.select_related(),
            pk=self.kwargs[POST_ID]
        )
        return super().form_valid(form)


class CommentUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    pk_url_kwarg = POST_ID


class CommentDeleteView(DeleteView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    pk_url_kwarg = POST_ID