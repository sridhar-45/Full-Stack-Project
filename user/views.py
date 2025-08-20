from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import re

import random
from django.core.mail import send_mail
from .models import EmailVerification
from django.conf import settings
from django.shortcuts import get_object_or_404


def home_view(request):
    return render(request, "home.html")


# Create your views here.
def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

       
        # Password validation
        if (
            len(password) < 8 or 
           not re.search(r"[A-Z]", password) or    
           not re.search(r"[a-z]", password) or 
           not re.search(r"[0-9]", password) or 
           not re.search(r"[!@#$%^&*]", password)
        ):
           messages.error(request, "Password is not strong enough")
           return redirect("user:register")

        if password != confirm_password:
            messages.error(request, "Password do not match")
            return redirect("user:register")
        

        if User.objects.filter(username = username).exists():
            messages.error(request, "username already exists")
            return redirect("user:register")
        
        user  = User.objects.create_user(username=username, email=email, password=password, is_active = False)

        #generate 6-digit code
        code = str(random.randint(100000, 999999))

        #save in database
        EmailVerification.objects.create(user = user, code = code)

        #send email
        send_mail (
            "Verfiy your emial",
            f"Your verfication code is {code}",
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently= False,
        )
        return redirect("user:verify")
    
        # user = User.objects.create_user(username = username, email = email, password = password)
        # user.save()
        
        messages.success(request, "Account created successfully! Please login.")
        return redirect("user:login")
    
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
            return redirect("user:login")

    return render(request, "user/login.html")


def logout_view(request):
    logout(request)
    return redirect("user:login")


def verify_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        code = request.POST["code"]

        user = get_object_or_404(User, username = username)
        verification = EmailVerification.objects.filter(user = user, code = code).first()

        if verification:
            user.is_active = True
            user.save()
            verification.delete() #remove OTP after success
            messages.success(request, "Email Verified! you can now log in.")
            return redirect("user:login")
        else:
            messages.error(request, "Invalid verification code")
            return redirect("user:verify")

    return render(request, "user/verify.html")
    


