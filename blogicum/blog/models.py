from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.db.models.query import QuerySet

from core.models import PublishedModel


User = get_user_model() # При замене модели пользователя не придётся вносить изменения по всему проекту: вместо прежней модели функция будет возвращать новую
LENGTH = 256


class PostManager(models.Manager):
    """Менеджер модель Post"""
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().select_related(
            'category',
            'location',
            'author'
        ).filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=timezone.now()
        )


class Category(PublishedModel):
    title = models.CharField('Заголовок', max_length=LENGTH)
    description = models.TextField('Описание')
    slug = models.SlugField(
        'Идентификатор', unique=True,
        help_text=(
            'Идентификатор страницы для URL; '
            'разрешены символы латиницы, цифры, дефис и подчёркивание.'
        )
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title[:10]


class Location(PublishedModel):
    name = models.CharField('Название места', max_length=LENGTH)

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.title[:10]


class Post(PublishedModel):
    title = models.CharField('Заголовок', max_length=LENGTH)
    text = models.TextField('Текст')
    pub_date = models.DateTimeField(
        'Дата и время публикации',
        help_text=(
            'Если установить дату и время в будущем — '
            'можно делать отложенные публикации.'
        )
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        related_name='posts',
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='posts',
        verbose_name='Категория'
    )
    # В модели `Post` создайте поле типа `ImageField`, которое служит для хранения изображения публикации
    image = models.ImageField('Изображение')

    objects = models.Manager()
    post_objects = PostManager()

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ['-pub_date']

    def __str__(self):
        return self.title[:10]

# Убедитесь, что в файле `blog/models.py` объявлена модель комментария с полем `ForeignKey`, связывающим её с моделью `Post`
class Comment(models.Model):
    post=models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='Комментируемый пост'
    )
# В модели `Comment` создайте поле типа `ForeignKey`, которое задаёт автора комментария, связывая модель `blog.models.Comment` с моделью `blog.models.Post`. User??
    author=models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария'        
    )
# В модели `Comment` создайте поле типа `TextField`, которое задаёт текст комментария
    text=models.TextField('Текст комментария')
# В модели `Comment` создайте поле типа `DateTimeField`, которое задаёт дату комментария
# В модели `Comment` в атрибуте `created_at` проверьте значение параметра `auto_now_add` на соответствие заданию
    created_at=models.DateTimeField(
        'Дата комментария',
         auto_now_add=True
         )