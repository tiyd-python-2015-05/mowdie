from django.shortcuts import render
from .models import Update
from django.contrib.auth.models import User


def index(request):
    updates = Update.objects.order_by('-posted_at')
    return render(request,
                  "updates/index.html",
                  {"updates": updates})


def show_status(request, status_id):
    update = Update.objects.get(pk=status_id)
    return render(request,
                  "updates/update.html",
                  {"update": update})


def show_user(request, user_id):
    user = User.objects.get(pk=user_id)
    updates = user.update_set.all().order_by('-posted_at')
    return render(request,
                  "updates/user.html",
                  {"user": user,
                   "updates": updates})
