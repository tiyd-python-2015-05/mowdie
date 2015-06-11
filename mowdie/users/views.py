from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

# Create your views here.
from users.forms import UserForm


def user_register(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            password = user.password

            # The form doesn't know to call this special method on user.
            user.set_password(password)
            user.save()

            # You must call authenticate before login. :(
            user = authenticate(username=user.username,
                                password=password)
            login(request, user)
            return redirect('index')
    else:
        form = UserForm()
    return render(request, "users/register.html", {'form': form})