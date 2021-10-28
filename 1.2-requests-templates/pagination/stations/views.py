import os
from csv import DictReader

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):

    context = dict()

    file_path = os.path.join(os.path.dirname(__file__), '..', 'data-398-2018-08-30.csv')
    bus_stations = list()
    with open(file_path, encoding='utf-8') as file:
        reader = DictReader(file)
        for row in reader:
            bus_station = dict()
            bus_station['Name'] = row['Name']
            bus_station['Street'] = row['Street']
            bus_station['District'] = row['District']
            bus_stations.append(bus_station)

    paginator = Paginator(bus_stations, 10)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    context['page'] = page
    context['bus_stations'] = page.object_list

    return render(request, 'stations/index.html', context)
