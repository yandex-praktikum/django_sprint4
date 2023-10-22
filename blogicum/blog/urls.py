from django.urls import path, include

from . import views

app_name = 'blog'
# Главная страница
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('posts/<int:id>/', views.DeleteView.as_view(), name='post_detail'),
    path('category/<slug:category_slug>/',
         views.category_posts, name='category_posts'),
]
