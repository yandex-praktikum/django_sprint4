from django.shortcuts import get_object_or_404, render
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)

from blog.models import Post, Category
from .forms import CommentForm

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
