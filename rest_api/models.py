from django.db import models
# from rest_api.managers import PublicationManager
from django.db.models import Count

from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])

class User(models.Model):
    name = models.CharField(max_length=128, verbose_name='Никнейм')
    birthday = models.DateField(verbose_name='Дата рождения')
    registration_date = models.DateField(verbose_name='Дата регистрации')
    email = models.EmailField(verbose_name='Email')
    avatar = models.ForeignKey('Pictures', null=True, blank=True,
                               verbose_name='Аватарка', on_delete=models.SET_NULL)
    description = models.TextField(
        null=True, blank=True, verbose_name='Описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['name']


class Subscription(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор', related_name='author')
    subscriber = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Подписчик', related_name='subscriber')
    date = models.DateTimeField(
        verbose_name='Дата подписки', auto_now_add=True)

    def __str__(self):
        return (self.author + '-' + self.subscriber)

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


class PublicationManager(models.Manager):
    def most_popular(self):
        return self.annotate(count_likes=Count('likes')).order_by('-count_likes')
    def most_popular_comments(self, obj):
        return Comment.objects.filter(publication=obj).annotate(count_likes=Count('likes')).order_by('-count_likes')

class Publication(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор')
    title = models.CharField(
        max_length=1024, verbose_name='Заголовок', null=True, blank=True)
    description = models.TextField(
        verbose_name='Описание', null=True, blank=True)
    date = models.DateTimeField(
        verbose_name='Дата создания', auto_now_add=True)

    objects = PublicationManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'


class Pictures(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор')
    publication = models.ForeignKey(
        Publication, on_delete=models.CASCADE, verbose_name='Публикация', null=True, blank=True)
    photo = models.ImageField(upload_to='photo')

    def __str__(self):
        return self.photo.name

    class Meta:
        verbose_name = 'Картинка'
        verbose_name_plural = 'Картинки'


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор')
    publication = models.ForeignKey(
        Publication, related_name='comments', on_delete=models.CASCADE, verbose_name='Публиация')
    comment = models.TextField(verbose_name='Комментарий')
    date = models.DateTimeField(
        verbose_name='Время комментария', auto_now_add=True)

    def __str__(self):
        return self.comment

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Like(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор')
    publication = models.ForeignKey(
        Publication, related_name='likes', on_delete=models.CASCADE, verbose_name='Публиация', null=True, blank=True)
    comment = models.ForeignKey(
        Comment, related_name='likes', on_delete=models.CASCADE, verbose_name='Комментарий', null=True, blank=True)
    date = models.DateTimeField(
        verbose_name='Время комментария', auto_now_add=True)

    def __str__(self):
        if self.comment != None:
            return self.comment
        return self.publication

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'
        unique_together = ('author', 'publication', 'comment')


class Tag(models.Model):
    publication = models.ManyToManyField(
        Publication, verbose_name='Публиация', blank=True)
    title = models.CharField(
        max_length=128, verbose_name='Заголовок', null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
