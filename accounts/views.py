from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import render
from django.shortcuts import redirect
from .models import CustomUser


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            if 'user' not in request.session:
                request.session['user'] = request.user.id
            messages.success(request, 'successfully login')
        else:
            messages.error(request, "username or password is incorrect")
        return redirect('auctions:index')

    else:
        return render(request, "accounts/login.html")


def logout_view(request):
    user_session = request.session['user']
    logout(request)
    request.session['user'] = user_session
    messages.success(request, "successfully logout")
    return redirect('auctions:index')


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            messages.error(request, 'password is not match')
            return redirect('accounts:register')

        # Attempt to create new user
        try:
            user = CustomUser.objects.create_user(username, email, password)
            user.save()
            messages.success(request, 'successfully register')
        except IntegrityError:
            messages.error(request, 'username already taken')
        else:
            login(request, user)
            if 'user' not in request.session:
                request.session['user'] = request.user.id
            return redirect('auctions:index')
    else:
        return render(request, "accounts/register.html")
