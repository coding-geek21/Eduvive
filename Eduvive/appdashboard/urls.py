from django.urls import path
from . import views
from .views import *
from .views import AddBlogView

urlpatterns = [
    path('',views.home,name='home'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('blogs/',views.blogs, name='blogs'),
    path('blog_content/<slug>', views.blog_content, name='blog_content'),
    path('add_blogs/' ,AddBlogView.as_view(), name='add_blogs'),
    path('update_blogs/<slug>',views.update_blogs,name='update_blogs'),
    path('view_blogs/',views.view_blog,name='view_blogs'),
    path('blog_delete/<id>',views.blog_delete,name='blog_delete'),
]
