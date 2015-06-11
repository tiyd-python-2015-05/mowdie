from django.db.models import Count
from django.shortcuts import render
from .models import Status
from django.contrib.auth.models import User


def index(request):
    statuses = Status.objects.annotate(Count('favorite')).order_by('-posted_at')
    return render(request,
                  "updates/index.html",
                  {"statuses": statuses})


def show_status(request, status_id):
    status = Status.objects.get(pk=status_id)
    return render(request,
                  "updates/status.html",
                  {"status": status})


def show_user(request, user_id):
    user = User.objects.get(pk=user_id)
    statuses = user.status_set.all().order_by('-posted_at')
    return render(request,
                  "updates/user.html",
                  {"user": user,
                   "statuses": statuses})
