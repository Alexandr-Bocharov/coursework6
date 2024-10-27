from django.contrib.auth.views import LogoutView
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView
from .models import User
from django.urls import reverse_lazy
from users.forms import UserRegisterForm, EditUserForm
import secrets
from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}/'
        send_mail(
            'Верификация почты',
            f'Чтобы подтвердить вашу почту для сайта <<Mail Sender>> перейдите по ссылке: {url}',
            EMAIL_HOST_USER,
            [user.email]
        )

        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse_lazy('users:login'))



class EditUserView(UpdateView):
    model = User
    form_class = EditUserForm
    success_url = reverse_lazy('users:edit')

    def get_object(self):
        return self.request.user



