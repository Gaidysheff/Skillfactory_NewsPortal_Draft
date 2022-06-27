from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect, render
from .models import * 


menu = ["О сайте", "Добавить статью", "Обратная связь", "Войти"]

def index(request):
    posts = Post.objects.all()
    return render(request, 'newsapp/index.html', {'posts': posts, 'menu': menu, 'title': 'Главная страница'})

def about(request):
    return render(request, 'newsapp/about.html', {'menu': menu, 'title': 'О сайте'})

def categories(request, cat):
    return HttpResponse(f"<h1>Статьи по категориям</h1>{cat}</p>")

def archive(request, year):
    if(int(year) > 2022):
        raise redirect('/', permanent=True)
    return HttpResponse(f"<h1>Архив по годам</h1>{year}</p>")

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
