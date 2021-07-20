from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request,'EduviveData/index.html')


def about(request):
    return render(request,'EduviveData/about.html')

def contact(request):
    return render(request,'EduviveData/contact.html')

