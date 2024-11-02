from django.db import models
from newsletter.models import NULLABLE
import os
from uuid import uuid4


def blog_image_upload_path(instance, filename):
    # Путь для изображений блогов
    return os.path.join('blog/', f"{uuid4()}_{filename}")


class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name='заголовок')
    body = models.TextField()
    photo = models.ImageField(verbose_name='изображение', upload_to='blog/', **NULLABLE)
    views_count = models.IntegerField(default=0, verbose_name='счетчик просмотров')
    published_date = models.DateTimeField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'блог'
        verbose_name_plural = 'блоги'
