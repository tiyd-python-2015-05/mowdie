from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages

# Create your views here.
from django.views.generic import ListView
from users.forms import UserForm, ProfileForm
from users.models import get_profile


class UserListView(ListView):
    model = User
    paginate_by = 10
    context_object_name = 'users'
    template_name = 'users/user_list.html'


def show_user(request, user_id):
    user = User.objects.get(pk=user_id)
    updates = user.update_set.all().order_by('-posted_at')
    return render(request,
                  "updates/user.html",
                  {"user": user,
                   "updates": updates})


@login_required
def edit_profile(request):
    profile = get_profile(request.user)

    if request.method == "GET":
        profile_form = ProfileForm(instance=profile)
    elif request.method == "POST":
        profile_form = ProfileForm(instance=profile, data=request.POST)
        if profile_form.is_valid():
            profile_form.save()
            messages.add_message(request, messages.SUCCESS,
                                 "Your profile has been updated.")

    return render(request, "users/edit_profile.html", {"form": profile_form})


@login_required
def follow_user(request, user_id):
    follower = get_profile(request.user, save=True)
    user_to_follow = get_object_or_404(User, pk=user_id)
    profile_to_follow = get_profile(user_to_follow, save=True)

    follower.followed.add(profile_to_follow)
    messages.add_message(request, messages.SUCCESS,
                         "You have followed this user.")
    return redirect('show_user', user_to_follow.id)


def user_register(request):
    if request.method == "GET":
        user_form = UserForm()
        profile_form = ProfileForm()
    elif request.method == "POST":
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            password = user.password
            # The form doesn't know to call this special method on user.
            user.set_password(password)
            user.save()

            # You must call authenticate before login. :(
            user = authenticate(username=user.username,
                                password=password)
            login(request, user)
            messages.add_message(
                request,
                messages.SUCCESS,
                "Congratulations, {}, on creating your new account! You are now logged in.".format(
                    user.username))
            return redirect('index')
    return render(request, "users/register.html", {'user_form': user_form,
                                                   'profile_form': profile_form})
