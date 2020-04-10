from django.shortcuts import render
from django.contrib.auth import login, authenticate,logout
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from .models import Profile,Journey
# Create your views here.

def home_view(request):
    if(request.method=='POST'):
        trip = Journey()
        trip.source=request.POST['source']
        trip.destination = request.POST['destination']
        trip.timefield = request.POST['time']
        trip.datefield = request.POST['date']
        trip.preference = request.POST['nopeople']
        trip.status = 'Upcoming'
        trip.profilename = request.user
        trip.save()
    
    profile = Profile.objects.filter(user=request.user)
    journey = Journey.objects.filter(profilename=request.user)
    print(journey)
    return render(request,'home.html',{'profile':profile,'journey':journey})

def logout_view(request):
    logout(request)
    return redirect(login_view)

def signup_view(request):
    if request.method=='POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user= form.save()
            user.refresh_from_db()
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.email = form .cleaned_data.get('email')
            user.profile.category = form.cleaned_data.get('category')        
            user.profile.phone = form.cleaned_data.get('phone')    
            user.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
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