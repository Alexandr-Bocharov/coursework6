from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin
from random import shuffle
from blog.models import Blog

from newsletter.forms import NewsletterForm, ClientForm, MessageForm
from newsletter.models import NewsLetter, Client, Message, DeliveryAttempt
from newsletter.scheduler import schedule_newsletter, unschedule_newsletter

from django.core.exceptions import PermissionDenied


# class NewsLetterListView(ListView):
#     model = NewsLetter

def home(request):
    all_newsletters_count = len(NewsLetter.objects.all())
    active_newsletters = len(NewsLetter.objects.filter(status=NewsLetter.Status.IN_PROGRESS))
    unique_clients = len(set([el.email for el in Client.objects.all()]))
    random_blog_posts = list(Blog.objects.all())
    shuffle(random_blog_posts)
    random_blog_posts = random_blog_posts[:3]

    content = {
        'all_newsletters_count': all_newsletters_count,
        'active_newsletters': active_newsletters,
        'unique_clients': unique_clients,
        'random_blog_posts': random_blog_posts,
    }
    return render(request, 'newsletter/home.html', content)


class NewsLetterCreateView(LoginRequiredMixin, CreateView):
    model = NewsLetter
    form_class = NewsletterForm
    success_url = reverse_lazy('newsletter:newsletter_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['clients'] = Client.objects.all()
        return context_data

    def form_valid(self, form):
        form.instance.user_owner = self.request.user

        newsletter = form.save()
        if newsletter.status == NewsLetter.Status.PENDING:
            newsletter.status = NewsLetter.Status.IN_PROGRESS
            newsletter.save()
            schedule_newsletter(newsletter)
        return super().form_valid(form)




def toggle_newsletter(request, pk):
    newsletter = get_object_or_404(NewsLetter, pk=pk)

    # Если статус в процессе, остановим задачу
    if newsletter.status == NewsLetter.Status.IN_PROGRESS:
        unschedule_newsletter(newsletter.id)  # Остановить задачу
        newsletter.status = NewsLetter.Status.COMPLETED  # Установить статус завершено
    elif newsletter.status == NewsLetter.Status.PENDING:
        schedule_newsletter(newsletter)  # Запустить задачу
        newsletter.status = NewsLetter.Status.IN_PROGRESS  # Установить статус в процессе

    newsletter.save()
    return redirect('newsletter:newsletter_list')


class NewsLetterUpdateView(LoginRequiredMixin, UpdateView):
    model = NewsLetter
    form_class = NewsletterForm
    fields = ('first_sending_dt', 'interval', 'clients')
    success_url = reverse_lazy('newsletter:home')

    def get_form_class(self):
        user = self.request.user
        if user == self.object.user_owner:
            return NewsletterForm
        raise PermissionDenied

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class NewsLetterListView(LoginRequiredMixin, ListView):
    model = NewsLetter

    def get_queryset(self):
        cur_user = self.request.user
        if cur_user.has_perm('newsletter.can_see_all_newsletters'):
            return NewsLetter.objects.all()
        return NewsLetter.objects.filter(user_owner=cur_user)


class NewsLetterDeleteView(LoginRequiredMixin, DeleteView):
    model = NewsLetter
    success_url = reverse_lazy('newsletter:newsletter_list')


class NewsLetterDetailView(LoginRequiredMixin, DetailView):
    model = NewsLetter


class DeliveryAttemptListView(LoginRequiredMixin, ListView):
    model = DeliveryAttempt
    ordering = ['-attempt_time']


class ClientListView(LoginRequiredMixin, ListView):
    model = Client

    def get_queryset(self):
        return Client.objects.filter(user_owner=self.request.user)


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('newsletter:client_list')

    def form_valid(self, form):
        form.instance.user_owner = self.request.user

        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    fields = ('name', 'email', 'comment')
    success_url = reverse_lazy('newsletter:client_list')


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('newsletter:client_list')


class MessageListView(LoginRequiredMixin, ListView):
    model = Message

    def get_queryset(self):
        return Message.objects.filter(user_owner=self.request.user)


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('newsletter:message_list')

    def form_valid(self, form):
        form.instance.user_owner = self.request.user

        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    fields = ('title', 'body')
    success_url = reverse_lazy('newsletter:message_list')

    def form_valid(self, form):
        user = self.request.user
        if user == self.object.user_owner:
            return MessageForm
        raise PermissionDenied



class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('newsletter:message_list')
