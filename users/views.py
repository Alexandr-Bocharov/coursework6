from django.contrib.auth.decorators import permission_required

from django.contrib.auth.views import LogoutView
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView, ListView
from .models import User
from django.urls import reverse_lazy
from users.forms import UserRegisterForm, EditUserForm, ManagerEditUserForm
import secrets
from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER

from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin


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

    success_url = reverse_lazy('users:edit')

    def get_object(self):
        return self.request.user

    def get_form_class(self):
        cur_user = self.request.user
        if cur_user.has_perm('users.can_blocked_users'):
            return ManagerEditUserForm
        else:
            return EditUserForm


class UserListView(LoginRequiredMixin, ListView):
    model = User

    def get_queryset(self):
        user = self.request.user
        admin = User.objects.get(email='admin@sky.com')
        if user.has_perm('users.can_see_all_users'):
            return User.objects.exclude(id=admin.id)
        else:
            raise PermissionDenied

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_see_all_users'] = self.request.user.has_perm('users.can_see_all_users')
        return context


@permission_required('users.can_blocked_users')
def block_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.is_active = not user.is_active
    user.save()
    return redirect('users:user_list')



