from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):

    CATEGORIES = (
        ('Танки', 'Танки'),
        ('Хилы', 'Хилы'),
        ('ДД', 'ДД'),
        ('Торговцы', 'Торговцы'),
        ('Гилдмастеры', 'Гилдмастеры'),
        ('Квестгиверы', 'Квестгиверы'),
        ('Кузнецы', 'Кузнецы'),
        ('Кожевники', 'Кожевники'),
        ('Зельевары', 'Зельевары'),
        ('Мастера заклинаний', 'Мастера заклинаний'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    text = RichTextUploadingField()
    category = models.CharField(max_length=18, choices=CATEGORIES)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})


class Response(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.post.user} - {self.text}'

    def get_absolute_url(self):
        return reverse('response_list', kwargs={'pk': self.pk})


class Newsletter(models.Model):
    title = models.CharField(max_length=128)
    text = models.TextField()

    def __str__(self):
        return f'{self.title}'
