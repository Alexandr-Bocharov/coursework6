from django import forms
from .models import NewsLetter, Client, Message


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsLetter
        fields = ['first_sending_dt', 'interval', 'status', 'clients', 'message']
        widgets = {
            'first_sending_dt': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

# class NewsletterForm(forms.ModelForm):
#     class Meta:
#         model = NewsLetter
#         fields = ('first_sending_dt', 'interval', 'clients', 'message')


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('name', 'email', 'comment')


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('title', 'body')
