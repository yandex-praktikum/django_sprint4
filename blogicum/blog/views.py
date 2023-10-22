from django.shortcuts import get_object_or_404, render

from blog.models import Post, Category

POSTS_LIMIT = 5


def index(request):
    '''
    Главная страница
    '''
    template = 'blog/index.html'
    post_list = Post.post_objects.select_related(
    )[:POSTS_LIMIT]
    context = {'post_list': post_list}
    return render(request, template, context)


def post_detail(request, id):
    '''
    Страница постов
    '''
    template = 'blog/detail.html'
    post = get_object_or_404(
        Post.post_objects,
        pk=id
    )
    context = {'post': post}
    return render(request, template, context)


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
