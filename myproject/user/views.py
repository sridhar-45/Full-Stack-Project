from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def home_view(request):
    return render(request, "home.html")


# Create your views here.
def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]


        if password != confirm_password:
            messages.error(request, "Password do not match")
            return redirect("register")
        

        if User.objects.filter(username = username).exists():
            messages.error(request, "username already exists")
            return redirect("register")
        
        user = User.Objects.create_user(Username = username, email = email, password = password)
        user.save()
        messages.success(request, "Account created successfully! Please login.")
        return redirect("login")
    
    return render(request, "user/register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password  = request.POST["password"]

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect("/") #redirect to home
        else:
            messages.error(request, "Invalid username or password")
            return redirect("login")

    return render(request, "user/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")