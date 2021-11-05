from django.views.generic import ListView
from django.shortcuts import render

from .models import Student


def students_list(request):
    template = 'school/students_list.html'
    context = {}

    ordering = 'group'
    context['students'] = Student.objects.all().order_by(ordering).prefetch_related('teachers')

    return render(request, template, context)
