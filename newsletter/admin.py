from django.contrib import admin

from newsletter.models import NewsLetter, Client, Message, Interval


@admin.register(NewsLetter)
class NewsLetterAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_sending_dt', 'interval', 'status')

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('title',)

@admin.register(Interval)
class IntervalAdmin(admin.ModelAdmin):
    list_display = ('name', 'frequency')


