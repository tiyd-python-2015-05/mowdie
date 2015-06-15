from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

# Create your views here.
from users.forms import UserForm, ProfileForm
from users.models import Profile


@login_required
def edit_profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)

    if request.method == "GET":
        profile_form = ProfileForm(instance=profile)
    elif request.method == "POST":
        profile_form = ProfileForm(instance=profile, data=request.POST)
        if profile_form.is_valid():
            profile_form.save()
            messages.add_message(request, messages.SUCCESS,
                                 "Your profile has been updated.")

    return render(request, "users/edit_profile.html", {"form": profile_form})


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
