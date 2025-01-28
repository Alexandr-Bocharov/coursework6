from django.urls import path
from blog.views import BlogListView, BlogDetailView
from blog.apps import BlogConfig
from django.views.decorators.cache import cache_page

app_name = BlogConfig.name

urlpatterns = [
    path('blog_list/', cache_page(60)(BlogListView.as_view()), name='blog_list'),
    path('blog_view/<int:pk>', BlogDetailView.as_view(), name='blog_view'),
]