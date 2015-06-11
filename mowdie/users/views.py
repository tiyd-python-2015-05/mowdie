from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

# Create your views here.

def user_login(request):
    if request.method == "POST":
        # 4C: Why do we use .get here instead of []?
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return redirect('index')
        else:
            # disabled account
            return render(request, "users/login.html",
                          {"failed": True, "username": username})
    else:
        return render(request, "users/login.html")
