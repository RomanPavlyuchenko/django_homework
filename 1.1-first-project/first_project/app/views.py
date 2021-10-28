from django.http import HttpResponse
from django.shortcuts import render, reverse
from datetime import datetime
from os import listdir


def home_view(request):
    template_name = 'app/home.html'
    pages = {
        'Главная страница': reverse('home'),
        'Показать текущее время': reverse('time'),
        'Показать содержимое рабочей директории': reverse('workdir')
    }

    context = {
        'pages': pages
    }
    return render(request, template_name, context)


def time_view(request):
    current_time = datetime.now()
    msg = f'Текущее время: {current_time.hour}:{current_time.minute}:{current_time.second}'
    return HttpResponse(msg)


def workdir_view(request):
    list_dir = listdir('.')
    msg = ''.join(f'{x}<br> ' for x in list_dir)
    return HttpResponse(msg)
