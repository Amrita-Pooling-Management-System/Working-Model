from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import SignUpForm
# Create your views here.

def home_view(request):
    return render(request,'home.html')

def signup_view(request):
    if request.method=='POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user= form.save()
            user.refresh_from_db()
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.email = form .cleaned_data.get('email')
            user.save()
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password1')
            user = authenticate(username=username,password=password)
            login(request,user)
            return redirect('home_view')
        else:
            return render(request,'signup.html',{'form':form})
    else:
        form= SignUpForm()
    return render(request,'signup.html',{'form':form})

def login_view(request):
    if request.method=='POST':
        username = request.POST["username"]
        password = request.POST["password"]
        print(username)
        user = authenticate(username=username,password=password)
        print(user)
        if user is not None:
            if user.is_active:
                login(request,user)
                return redirect('home_view')

            else:
                return render(request,'login.html', {'err': 'Your account is blocked'})
        else:
            return render(request,'login.html',{'err': 'Wrong credentials provided'})
    else:
        return render(request,'login.html',{'err': ''})