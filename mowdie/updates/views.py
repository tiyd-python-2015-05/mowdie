from django.shortcuts import render
from django.http import HttpResponse
from .models import Status
from django.contrib.auth.models import User

# Create your views here.

def all_statuses(request):
    statuses = Status.objects.all().order_by('-posted_at')
    return render(request,
                  "updates/all_statuses.html",
                  {"statuses": statuses})


def show_user(request, user_id):
    user = User.objects.get(pk=user_id)
    statuses = user.status_set.all().order_by('-posted_at')
    return render(request,
                  "updates/user.html",
                  {"user": user,
                   "statuses": statuses})