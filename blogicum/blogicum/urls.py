from django.contrib import admin
from django.urls import path, include


handler404 = 'pages.views.page_not_found'
handler500 = 'pages.views.server_error'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('pages.urls')),
    path('', include('blog.urls'), name='index'),
    path('auth', include('django.contrib.auth.urls')),
]
