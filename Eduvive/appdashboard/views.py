from django.shortcuts import render
from .models import BlogModel
from django.contrib.auth.models import User
from django.shortcuts import render , redirect
from django.contrib import messages
from django.views import View
from .form import BlogForm
from django import forms
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required(login_url='login') 
def dashboard(request):
    return render(request,'appdashboard/dashboard.html')


@login_required(login_url='login') 
def blogs(request):
    context = {'trending_first':BlogModel.objects.all().filter(tag='trending_first'),
    'trending' : BlogModel.objects.all().filter(tag='trending'),
    'latest':BlogModel.objects.all().filter(tag='latest'),
    'editor1':BlogModel.objects.all().filter(tag='editor1'),
    'editor2':BlogModel.objects.all().filter(tag='editor2'),
    'popular':BlogModel.objects.all().filter(tag='popular')}
    return render(request , 'appdashboard/blogs.html',context)

@login_required(login_url='login') 
def view_blog(request):
    context = {}

    try:
        blog_objs = BlogModel.objects.filter(user=request.user)
        context['blog_objs'] = blog_objs
    except Exception as e:
        print(e)

    print(context)
    return render(request, 'appdashboard/view_blogs.html', context)

class AddBlogView(View):
    def get(self,request):
        context = {'form' : BlogForm}
        return render(request,'appdashboard/add_blogs.html',context)

    
    def post(self,request):
        context = {'form' : BlogForm}
        image = request.FILES['image']
        title = request.POST['title']
        tag=request.POST['tag']            
        user = request.user
        # content=request.POST['content']

        
        try:  
            form = BlogForm(request.POST)         
            if form.is_valid():
                content = form.cleaned_data['content']
                blog_obj = BlogModel.objects.create(
                user = user , title = title, 
                content = content, image = image, tag=tag
                )
                messages.success(request,"Your Blog is successfully Added!!")
                return redirect('add_blogs')

   
        except Exception as e :
            messages.error(request,"Error in adding your blog")
            print("exception",e)
    
        return render(request , 'appdashboard/add_blogs.html',context)



@login_required(login_url='login') 
def update_blogs(request, slug):
    context = {}
    try:

        blog_obj = BlogModel.objects.get(slug=slug)

        if blog_obj.user != request.user:
            return redirect('/')

        initial_dict = {'content': blog_obj.content}
        form = BlogForm(initial=initial_dict)
        if request.method == 'POST':
            form = BlogForm(request.POST)
            print(request.FILES)
            title = request.POST.get('title')
            user = request.user
            
            if form.is_valid():
                content = form.cleaned_data['content']

            blog_obj = BlogModel.objects.filter(slug=slug).update(
                user=user, title=title,
                content=content
            )

        context['blog_obj'] = blog_obj
        context['form'] = form
    except Exception as e:
        print(e)

    return render(request, 'appdashboard/update_blogs.html', context)


def blog_delete(request, id):
    try:
        blog_obj = BlogModel.objects.get(id=id)

        if blog_obj.user == request.user:
            blog_obj.delete()

    except Exception as e:
        print(e)

    return redirect('view_blogs')


@login_required(login_url='login') 
def blog_content(request,slug):
    context = {}
    try:
        blog_obj = BlogModel.objects.filter(slug = slug).first()
        context['blog_obj'] =  blog_obj
    except Exception as e:
        print(e)
    return render(request,'appdashboard/blog_content.html',context)


def home(request):
    return render(request,'appdashboard/index.html')   