from django.urls import path
from django.views.generic import TemplateView

app_name = 'pages'
# Убедитесь, что в файле `pages/urls.py` маршруты статических страниц подключены с помощью CBV
urlpatterns = [
    path('about/',
         TemplateView.as_view(template_name='pages/about.html'),
         name='about'),
    path('rules/', 
         TemplateView.as_view(template_name='pages/rules.html'),
         name='rules'),
]
