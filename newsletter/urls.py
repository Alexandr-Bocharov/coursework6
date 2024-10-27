from django.urls import path

from newsletter.apps import NewsletterConfig
from newsletter.views import NewsLetterCreateView, home, NewsLetterUpdateView, NewsLetterListView, ClientListView, \
    ClientDetailView, ClientCreateView, ClientUpdateView, ClientDeleteView, MessageListView, MessageDetailView, \
    MessageCreateView, MessageUpdateView, MessageDeleteView

app_name = NewsletterConfig.name

urlpatterns = [
    path('', home, name='home'),
    path('newsletter/create/', NewsLetterCreateView.as_view(), name='newsletter_create'),
    path('newsletter/edit/<int:pk>/', NewsLetterUpdateView.as_view(), name='newsletter_edit'),
    path('newsletter/list/', NewsLetterListView.as_view(), name='newsletter_list'),
    path('client/list/', ClientListView.as_view(), name='client_list'),
    path('client/detail/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('client/create/', ClientCreateView.as_view(), name='client_create'),
    path('client/edit/<int:pk>/', ClientUpdateView.as_view(), name='client_edit'),
    path('client/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
    path('message/list/', MessageListView.as_view(), name='message_list'),
    path('message/detail/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('message/create/', MessageCreateView.as_view(), name='message_create'),
    path('message/edit/<int:pk>/', MessageUpdateView.as_view(), name='message_edit'),
    path('message/delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),
]