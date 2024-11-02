from django.db import models
from django.utils import timezone
from users.models import User
import pytz

NULLABLE = {'blank': True, 'null': True}


class Message(models.Model):
    title = models.CharField(max_length=255, verbose_name='Тема письма')
    body = models.TextField()

    user_owner = models.ForeignKey(User, verbose_name='пользователь-владелец', on_delete=models.SET_NULL, **NULLABLE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'


class Client(models.Model):
    name = models.CharField(max_length=250, verbose_name='Ф.И.О.', **NULLABLE)
    email = models.EmailField(max_length=150, verbose_name='почта')
    comment = models.TextField(**NULLABLE, verbose_name='комментарий')

    user_owner = models.ForeignKey(User, verbose_name='пользователь-владелец', on_delete=models.SET_NULL, **NULLABLE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


class Interval(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название интервала")
    frequency = models.CharField(max_length=10, verbose_name="Частота")

    def __str__(self):
        return self.name


class NewsLetter(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Ожидание'
        IN_PROGRESS = 'in_progress', 'В процессе'
        COMPLETED = 'completed', 'Завершено'

    first_sending_dt = models.DateTimeField()
    last_sending_dt = models.DateTimeField()
    interval = models.ForeignKey(Interval, on_delete=models.CASCADE, verbose_name='интервал')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    clients = models.ManyToManyField(Client, related_name='news_letter')
    message = models.ForeignKey(Message, verbose_name='сообщение', on_delete=models.CASCADE, default=None)

    user_owner = models.ForeignKey(User, verbose_name='пользователь-владелец', on_delete=models.SET_NULL, **NULLABLE)

    def __str__(self):
        return f"Рассылка {self.interval}. C {self.first_sending_dt} до {self.last_sending_dt}"

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'
        permissions = [
            ('can_see_all_newsletters', 'can see all newsletters'),
            ('can_cancel_newsletter', 'can cancel newsletter'),
        ]


class DeliveryAttempt(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Ожидание'
        SUCCESS = 'success', 'Успешно'
        FAILED = 'failed', 'Неудачно'

    newsletter = models.ForeignKey(NewsLetter, on_delete=models.CASCADE, verbose_name='рассылка',
                                   related_name='delivery_attempts')
    attempt_time = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, verbose_name='статус', choices=Status.choices, default=Status.PENDING)
    response = models.TextField(verbose_name='Ответ сервера', **NULLABLE)

    user_owner = models.ForeignKey(User, verbose_name='пользователь-владелец', on_delete=models.SET_NULL, **NULLABLE)

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылки'

    def __str__(self):
        return f'Попытка для {self.newsletter} - {self.attempt_time} ({self.status})'
