from django.shortcuts import render, redirect
from .models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):
    template = 'catalog.html'
    context = {}
    phones = Phone.objects.all()

    is_sort = request.GET.get('sort')
    if is_sort:
        if is_sort == 'name':
            phones = phones.order_by('name')
        if is_sort == 'min_price':
            phones = phones.order_by('price')
        if is_sort == 'max_price':
            phones = phones.order_by('-price')

    context['phones'] = phones
    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'
    context = {'phone': Phone.objects.get(slug=slug)}
    return render(request, template, context)
