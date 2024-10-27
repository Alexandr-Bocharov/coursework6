from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Message(models.Model):
    title = models.CharField(max_length=255, verbose_name='Тема письма')
    body = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'


class Client(models.Model):
    name = models.CharField(max_length=250, verbose_name='Ф.И.О.')
    email = models.EmailField(max_length=150, verbose_name='почта', unique=True)
    comment = models.TextField(**NULLABLE, verbose_name='комментарий')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


class Interval(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название интервала")  # Например: 'Ежедневно'
    frequency = models.CharField(max_length=10, verbose_name="Частота")  # Например: 'daily', 'weekly', 'monthly'

    def __str__(self):
        return self.name


class NewsLetter(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Ожидание'
        IN_PROGRESS = 'in_progress', 'В процессе'
        COMPLETED = 'completed', 'Завершено'

    first_sending_dt = models.DateTimeField()
    interval = models.ForeignKey(Interval, on_delete=models.CASCADE, verbose_name='интервал')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    clients = models.ManyToManyField(Client, related_name='news_letter')
    message = models.ForeignKey(Message, verbose_name='сообщение', on_delete=models.CASCADE, default=None)



    def __str__(self):
        return f"Рассылка {self.interval} на {self.first_sending_dt}"

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'