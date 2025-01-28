from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from users.views import RegisterView, EditUserView, email_verification, UserListView, block_user

from users import apps

app_name = apps.UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('edit/', EditUserView.as_view(), name='edit'),
    path('user_list/', UserListView.as_view(), name='user_list'),
    path('users/<int:pk>/block/', block_user, name='block_user'),
    path('email-confirm/<str:token>/', email_verification, name='email-confirm'),
]