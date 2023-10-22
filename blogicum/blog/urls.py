from django.urls import path, include

from . import views

app_name = 'blog'
# Главная страница
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('posts/<int:id>/', views.DeleteView.as_view(), name='post_detail'),
    path('category/<slug:category_slug>/',
         views.category_posts, name='category_posts'),

# Профили
# Reverse for 'profile' not found. 'profile' is not a valid view function or pattern name
    path('profile/<str:username>',
         views.ProfileDetailView.as_view(), name='profile'),
# Reverse for 'create_post' not found. 'create_post' is not a valid view function or pattern name        
    path('profile/create/',
         views.PostCreateView.as_view(), name='create_post'),
# Reverse for 'edit_profile' not found. 'edit_profile' is not a valid view function or pattern name
    path('edit_profile/',
         views.ProfileUpdateView.as_view(), name='edit_profile'),
]
