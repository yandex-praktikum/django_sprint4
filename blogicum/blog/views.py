from typing import Any
from django.db import models
from django.http import HttpRequest, Http404
# Подключите к проекту пагинацию
from django.core.paginator import Paginator
from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, LoginRequiredMixin

from .models import Post, Category, User, Comment
from .forms import CommentForm, UserForm, PostForm

POST_ID = 'post_id'
COM_ID = 'comment_id'
# Настройте вывод не более 10 публикаций (переменная для пагинатора)
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

    def get_object(self):
        post = super().get_object()
        post_id = self.kwargs[POST_ID]
        if post.author == self.request.user:
            return get_object_or_404(
                Post.post_objects, pk=post_id
            )
        return get_object_or_404(
            Post.post_objects, pk=post_id
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comments.select_related('post')
        return context

# Создайте страницу для публикации новых записей posts/create/
# Reverse for 'create_post' not found. 'create_post' is not a valid view function or pattern name
# 'Location' object has no attribute 'title'
# Cannot assign "<SimpleLazyObject: <django.contrib.auth.models.AnonymousUser object at 0x000001FCC4C20220>>": "Post.author" must be a "User" instance.
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'

# No URL to redirect to.  Either provide a url or define a get_absolute_url method on the Model.
    def get_success_url(self):
        username = self.request.user.username
        return reverse_lazy('blog:profile', kwargs={'username': username})
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    pk_url_kwarg = POST_ID
    form_class = PostForm
    template_name = 'blog/create.html'

    def get_context_data(self, **kwargs):
        '''Вывод текста поста'''
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm(instance=self.object)
        return context
    
    def get_success_url(self):
# На несуществующую страницу поста, в профиль не получилось
        return reverse_lazy('blog:delete_post',
                            kwargs={'post_id': self.kwargs['post_id']})
    
# Убедитесь, что пользователь не может редактировать чужие посты
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    pk_url_kwarg = POST_ID
    form_class = PostForm
    template_name = 'blog/create.html'
# PostUpdateView is missing the implementation of the test_func() method
    def test_func(self):
        if self.request.user != self.get_object().author:
            return False
        return True
    
#    def get_success_url(self):
# На страницу обновленного поста
# Убедитесь, что при отправке формы редактирования поста неавторизованным пользователем он перенаправляется на страницу публикации (/posts/<int:post_id>/)
#        return reverse_lazy('blog:post_detail',
#                            kwargs={'post_id': self.kwargs['post_id']})

# Убедитесь, что пользователь не может редактировать чужие посты
    def handle_no_permission(self):
        return reverse_lazy('blog:post_detail',
                            kwargs={'post_id': self.kwargs['post_id']})


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
        object_list = Post.post_objects.filter(author=author)
# Все посты автора
        if self.request.user == author:
            object_list = Post.objects.all()
# Пагинация
        # object_list = object_list.filter(author=author)
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

# Cannot assign "<SimpleLazyObject: <django.contrib.auth.models.AnonymousUser object at 0x000001648248A2E0>>": "Comment.author" must be a "User" instance.
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(
            Post.post_objects.filter(
                is_published=True,
                category__is_published=True,
                pub_date__lte=timezone.now()
            ),
            pk=self.kwargs[POST_ID]
        )
        return super().form_valid(form)
# Редирект, по аналогии с No URL to redirect to.  Either provide a url or define a get_absolute_url method on the Model.
    def get_success_url(self):
        return reverse_lazy('blog:post_detail',
                            kwargs={'post_id': self.kwargs['post_id']})



class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    pk_url_kwarg = COM_ID
    form_class = PostForm
    template_name = 'blog/create.html'

    def test_func(self):
        if self.request.user != self.get_object().author:
            return False
        return True
# Убедитесь, что автору комментария видна ссылка на страницу редактирования этого комментария. Проверьте, что в словарь контекста для страницы редактирования комментария передаётся объект формы
    def handle_no_permission(self):
        #raise Http404('Страница не найдена')
        return reverse_lazy('blog:edit_comment',
                            kwargs={'post_id': self.kwargs['post_id']})

# Есть вариант реализации через dispatch
# Страницы удаления и редактирования комментария должны иметь идентичные права доступа. Убедитесь, что GET-запрос к этим страницам возвращает один и тот же статус и не удаляет комментарий
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    pk_url_kwarg = COM_ID
    form_class = PostForm
    template_name = 'blog/create.html'

# Страницы удаления и редактирования комментария должны иметь идентичные права доступа. Убедитесь, что GET-запрос к этим страницам возвращает один и тот же статус и не удаляет комментарий
# Относится к UserPassesTestMixin
    def test_func(self):
        if self.request.user != self.get_object().author:
            return False
        return True

    def handle_no_permission(self):
        #raise Http404('Страница не найдена')
        return reverse_lazy('blog:delete_comment',
                            kwargs={'post_id': self.kwargs['post_id']})

class CategoryPostListView(ListView):
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
        return (Post.post_objects.
                filter(category__slug=category.slug))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.object
        context['category'] = category
        return context