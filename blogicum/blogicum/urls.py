from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings


handler404 = 'pages.views.page_not_found'
handler500 = 'pages.views.server_error'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('pages.urls')),
    path('', include('blog.urls')),
# Reverse for 'login' not found. 'login' is not a valid view function or pattern name
    path('auth/', include('django.contrib.auth.urls')),
# Reverse for 'registration' not found. 'registration' is not a valid view function or pattern name
    path('auth/registration',
         CreateView.as_view(
             template_name='registration/registration_form.html',
             form_class=UserCreationForm,
# No URL to redirect to.  Either provide a url or define a get_absolute_url method on the Model
             success_url=reverse_lazy('blog:index'),
         ), name='registration',
    ),
]

if settings.DEBUG:
    import debug_toolbar
    # Добавить к списку urlpatterns список адресов из приложения debug_toolbar:
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)