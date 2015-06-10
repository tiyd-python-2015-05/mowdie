from django.shortcuts import render
from django.http import HttpResponse
from .models import Status

# Create your views here.

def all_statuses(request):
    statuses = Status.objects.all()
    status_strings = [str(status) for status in statuses]
    return HttpResponse("<br>".join(status_strings))
