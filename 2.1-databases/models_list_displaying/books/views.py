from django.shortcuts import render
from .models import Book


def books_view(request):
    template = 'books/books_list.html'
    context = {'books': Book.objects.all()}
    return render(request, template, context)


def book_view(request, dt):
    template = 'books/books_list.html'
    context = {}

    context['books'] = Book.objects.all().filter(pub_date=dt)

    prev_date = Book.objects.all().filter(pub_date__lt=dt).first()
    if prev_date:
        context['prev_date'] = prev_date.pub_date

    next_date = Book.objects.all().filter(pub_date__gt=dt).first()
    if next_date:
        context['next_date'] = next_date.pub_date

    return render(request, template, context)