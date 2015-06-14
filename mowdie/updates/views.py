from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.datetime_safe import datetime
from .models import Update
from django.contrib.auth.models import User

from .forms import UpdateForm


def index(request):
    updates = Update.objects.order_by('-posted_at')
    return render(request,
                  "updates/index.html",
                  {"updates": updates})


@login_required
def add_update(request):
    if request.method == "POST":
        form = UpdateForm(request.POST)
        if form.is_valid():
            update = form.save(commit=False)
            update.user = request.user
            update.posted_at = datetime.now()
            update.save()
            messages.add_message(request, messages.SUCCESS,
                                 "Your update was successfully posted!")
            return redirect("index")
    else:
        form = UpdateForm()

    return render(request, "updates/add.html", {"form": form})


def show_update(request, update_id):
    update = get_object_or_404(Update, pk=update_id)
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


@login_required
def add_favorite(request, update_id):
    update = get_object_or_404(Update, pk=update_id)
    if not update.favorite_set.filter(user=request.user).count():
        update.favorite_set.create(user=request.user)
    return redirect("show_update", update.id)
