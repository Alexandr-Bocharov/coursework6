from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from newsletter.forms import NewsletterForm, ClientForm, MessageForm
from newsletter.models import NewsLetter, Client, Message
from newsletter.services import send_clients_email


# class NewsLetterListView(ListView):
#     model = NewsLetter

def home(request):
    return render(request, 'newsletter/home.html')


class NewsLetterCreateView(CreateView):
    model = NewsLetter
    form_class = NewsletterForm
    success_url = reverse_lazy('newsletter:home')


    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['clients'] = Client.objects.all()
        return context_data


    def form_valid(self, form):
        newsletter = form.save()
        send_clients_email(newsletter)
        return super().form_valid(form)



class NewsLetterUpdateView(UpdateView):
    model = NewsLetter
    fields = ('first_sending_dt', 'interval', 'clients')
    success_url = reverse_lazy('newsletter:home')


class NewsLetterListView(ListView):
    model = NewsLetter





class ClientListView(ListView):
    model = Client


class ClientDetailView(DetailView):
    model = Client


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('newsletter:client_list')


class ClientUpdateView(UpdateView):
    model = Client
    fields = ('name', 'email', 'comment')
    success_url = reverse_lazy('newsletter:client_list')


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('newsletter:client_list')


class MessageListView(ListView):
    model = Message


class MessageDetailView(DetailView):
    model = Message


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('newsletter:message_list')


class MessageUpdateView(UpdateView):
    model = Message
    fields = ('title', 'body')
    success_url = reverse_lazy('newsletter:message_list')


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('newsletter:message_list')






