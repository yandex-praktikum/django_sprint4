from typing import Any
from django.db import models
from django.http import HttpRequest
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
    form_class = CommentForm
    template_name = 'blog/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comments.select_related('author')
        return context

    def get_object(self):
        post = super().get_object()
        post_id = self.kwargs[POST_ID]
        if post.author == self.request.user:
            return get_object_or_404(
                Post.post_objects.post_object(), pk=post_id
            )
        return get_object_or_404(
            Post.post_objects.published_posts(), pk=post_id
        )
# Создайте страницу для публикации новых записей posts/create/
# Reverse for 'create_post' not found. 'create_post' is not a valid view function or pattern name
# 'Location' object has no attribute 'title'
class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)



class PostDeleteView(DeleteView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    pk_url_kwarg = POST_ID
    success_url = reverse_lazy('blog:index')


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

    def get_context_data(self, **kwargs):
        author = self.object
        # Выводим только посты автора на профиле автора
        object_list = Post.post_objects.select_related()
        if self.request.user == author:
            # Выводим все посты автора на его собственном профиле
            object_list = Post.post_objects.post_object()
# Пагинация
        object_list = object_list.filter(author=author)
        context = super().get_context_data(**kwargs)
        page_num = self.request.GET.get('page', 1)
        paginator = Paginator(object_list, POSTS_LIMIT)
        context['page_obj'] = paginator.get_page(page_num)

        return context

 

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
    model = Post
    paginate_by = POSTS_LIMIT
    template_name = 'blog/category.html'

    def get(self, request: HttpRequest, *args, **kwargs):
        self.object = get_object_or_404(
            Category,
            slug=self.kwargs['category_slug'],
            is_published=True
        )
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        category = self.object
        return (Post.post_objects.select_related().
                filter(category__slug=category.slug))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.object
        context['category'] = category
        return context


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