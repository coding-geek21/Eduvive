from django.urls import path
from . import views
from .views import *
from .views import AddBlogView

urlpatterns = [
    path('dashboard/',views.dashboard, name='dashboard'),
    path('blogs/',views.blogs, name='blogs'),
    path('blog_content/<slug>', views.blog_content, name='blog_content'),
    path('add_blogs/' ,AddBlogView.as_view(), name='add_blogs'),
]
