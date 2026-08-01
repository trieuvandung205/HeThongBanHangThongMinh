from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from .forms import RegisterForm


def register(request):

    if request.method=="POST":

        form=RegisterForm(request.POST)

        if form.is_valid():

            user=form.save(commit=False)

            user.role="customer"

            user.save()

            login(request,user)

            return redirect("/")

    else:

        form=RegisterForm()

    return render(request,"accounts/register.html",{

        "form":form

    })


def user_login(request):

    error=None

    if request.method=="POST":

        username=request.POST.get("username")

        password=request.POST.get("password")

        user=authenticate(
            request,
            username=username,
            password=password
        )

        if user:

            login(request,user)

            if user.role=="admin":

                return redirect("dashboard")

            if user.role=="staff":

                return redirect("staff_dashboard")

            return redirect("/")

        error="Sai tên đăng nhập hoặc mật khẩu."

    return render(request,"accounts/login.html",{

        "error":error

    })


def user_logout(request):

    logout(request)

    return redirect("/")