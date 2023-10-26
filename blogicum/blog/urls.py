from django.urls import path, include

from . import views

app_name = 'blog'

urlpatterns = [
# Главная страница

    path('', views.IndexView.as_view(), name='index'),

# Профили
# Удобно разделить дочерние url по тематическим частям и заинклюдить к родительским, выглядит читабельней и аккуратней

# Reverse for 'profile' not found. 'profile' is not a valid view function or pattern name
    path('profile/<str:username>/',
         views.ProfileDetailView.as_view(), name='profile'),
# Reverse for 'edit_profile' not found. 'edit_profile' is not a valid view function or pattern name
    path('edit_profile/',
         views.ProfileUpdateView.as_view(), name='edit_profile'),

# Посты
# Reverse for 'create_post' not found. 'create_post' is not a valid view function or pattern name      
    path('posts/create/',
         views.PostCreateView.as_view(), name='create_post'),
    path('posts/<int:post_id>/',
         views.PostDetailView.as_view(), name='post_detail'),
    path('posts/<int:post_id>/edit/',
         views.PostUpdateView.as_view(), name='edit_post'),
    path('posts/<int:post_id>/delete/',
         views.PostDeleteView.as_view(), name='delete_post'),
    path('posts/<int:post_id>/comment',
         views.CommentCreateView.as_view(), name='add_comment'),
    path('posts/<int:post_id>/edit_comment/<comment_id>/',
         views.CommentUpdateView.as_view(), name='edit_comment'),
    path('posts/<int:post_id>/delete_comment/<comment_id>/',
         views.CommentDeleteView.as_view(), name='delete_comment'),

# Категории
    path('category/<slug:category_slug>/',
         views.CategoryPostListView.as_view(), name='category_posts'),
]
