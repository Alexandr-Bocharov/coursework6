from django import forms
from .models import NewsLetter, Client, Message


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsLetter
        fields = ['first_sending_dt', 'last_sending_dt', 'interval', 'status', 'clients', 'message']
        widgets = {
            'first_sending_dt': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'last_sending_dt': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

        self.fields['message'].queryset = Message.objects.filter(user_owner=self.user)
        self.fields['clients'].queryset = Client.objects.filter(user_owner=self.user)


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
