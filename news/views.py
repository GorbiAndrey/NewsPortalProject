from django.shortcuts import render
from .models import New


def index(request):
    news = New.objects.all()
    return render(request, 'index.html', context = {'news': news})

def detail(request, id):
    new = New.objects.get(id__iexact=id)
    return render(request, 'news.html', context={'new':new})

