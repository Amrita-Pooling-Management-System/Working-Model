from django.shortcuts import render
from django.contrib.auth import login, authenticate,logout
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from .models import Profile,Journey,Teams
from operator import itemgetter
import datetime
from threading import Timer
# Create your views here.
def home_view(request,pk=None):
    if pk:
        team=[]
        auto=[]
        jou=Journey.objects.filter(pk=pk)
        print(jou)
        team = Teams.objects.filter(jid=jou[0])
        print(len(team))
        if len(team)!=0:
            print(team[0].pid)
            use= User.objects.filter(username=team[0].pid)
            auto = Profile.objects.filter(user=use[0])
            print(auto)
    else:
        team=[]
        auto=[]
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
    return render(request,'home.html',{'profile':profile,'journey':journey,'team':team,'auto':auto})

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

def auto_view(request,pk=None):
    pro=Profile.objects.filter(user=request.user)
    team=Teams.objects.filter(pid=pro[0])
    j=[]
    te=[]
    max=0
    if pk:
        j=Teams.objects.filter(teamid=pk)
    if(request.method=='POST'):
        auto=Profile.objects.get(user=request.user)
        auto.signup_confirmation=False
        auto.save()
    for t in team:
        if max!=t.teamid:
            te.append(t)
            max=t.teamid
    print(te)
    return render(request,'auto.html',{'journey':j,'profile':pro,'team':te})


def login_view(request):
    if request.method=='POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username,password=password)
        if user is not None:
            if user.is_active:
                login(request,user)
                profile = Profile.objects.filter(user=request.user)
                cat=profile[0].category
                if(cat=='DRIV'):
                    return redirect('auto_view')
                return redirect('home_view')

            else:
                return render(request,'login.html', {'err': 'Your account is blocked'})
        else:
            return render(request,'login.html',{'err': 'Wrong credentials provided'})
    else:
        return render(request,'login.html',{'err': ''})

def teamform(date):
    ndate = datetime.datetime.strptime(date, '%Y-%m-%d')
    print(ndate.date())
    list = Journey.objects.filter(datefield=ndate.date(),status='Upcoming')
    print(list)
    kayam={}
    karu={}
    valli={}
    for item in list:
        print(item.source)
        if(item.source.lower()=='kayamkulam' or item.source.lower()=='kyj'):
            kayam[item.id]=item.timefield
        elif(item.source.lower()=='karunagapalli' or item.source.lower()=='kpi'):
            karu[item.id]=item.timefield
        elif(item.source.lower()=='vallikavu' or item.source.lower()=='val'):
            valli[item.id]=item.timefield
    kayam = sorted(kayam.items(),key = itemgetter(1))
    karu = sorted(karu.items(),key = itemgetter(1))
    valli = sorted(valli.items(),key = itemgetter(1))
    drivers=Profile.objects.filter(category='DRIV')
    i=0
    time=0
    if not Teams.objects.all().last():
        k=1
    else:
        k=(Teams.objects.all().last().teamid)+1
    for item in drivers:
        print(item.signup_confirmation)
        if(item.signup_confirmation==False):
            if(len(kayam)!=0 and i<len(kayam)):
                for j in range(0,len(kayam)):
                    tea=Teams();
                    i+=1
                    if(j!=0 and j%4==0):
                        k+=1
                        break

                    else:
                        for item1 in Journey.objects.filter(pk=kayam[j][0]):
                            tea.jid=item1
                            item1.status='DONE'
                            item1.save()
                        tea.pid=item
                        tea.teamid=k
                        item.signup_confirmation=True
                        item.save()
                        tea.save()
                        if(j+1<len(kayam)):
                            date = datetime.date(1, 1, 1)
                            datetime1 = datetime.datetime.combine(date, kayam[j+1][1])
                            datetime2 = datetime.datetime.combine(date, kayam[j][1])
                            diff = datetime1 - datetime2
                            tot=diff.total_seconds()
                            mint=tot/60
                            if mint>60:
                                print(kayam[j])
                                i-=1
                                k+=1
                                kayam.pop(j)
                                break

                    print(i)
            elif(len(karu)!=0 and i-len(kayam)<len(karu)):
                k+=1
                for j in range(0,len(karu)):
                    tea1=Teams();
                    i+=1
                    if(j!=0 and j%4==0):
                        k+=1
                        break
                    else:
                        for item2 in Journey.objects.filter(pk=karu[j][0]):
                            tea1.jid=item2
                            item2.status='DONE'
                            item2.save()
                        tea1.pid=item
                        item.signup_confirmation=True
                        tea1.teamid=k
                        item.save()
                        tea1.save()
                        if(j+1<len(karu)):
                            date = datetime.date(1, 1, 1)
                            datetime1 = datetime.datetime.combine(date, karu[j+1][1])
                            datetime2 = datetime.datetime.combine(date, karu[j][1])
                            diff = datetime1 - datetime2
                            tot=diff.total_seconds()
                            mint=tot/60
                            if mint>60:
                                i-=1
                                k+=1
                                karu.pop(j)
                                break
            elif(len(valli)!=0 and i-len(kayam)-len(karu)<len(valli)):
                k+=1
                for j in range(0,len(valli)):
                    tea2=Teams();
                    i+=1
                    if(j!=0 and j%4==0):
                        k+=1
                        break
                    else:

                        for item2 in Journey.objects.filter(pk=valli[j][0]):
                            tea2.jid=item2
                            item2.status='DONE'
                            item2.save()
                        tea2.pid=item
                        item.signup_confirmation=True
                        tea2.teamid=k
                        item.save()
                        tea2.save()
                        if(j+1<len(valli)):
                            date = datetime.date(1, 1, 1)
                            datetime1 = datetime.datetime.combine(date, valli[j+1][1])
                            datetime2 = datetime.datetime.combine(date, valli[j][1])
                            diff = datetime1 - datetime2
                            tot=diff.total_seconds()
                            mint=tot/60
                            if mint>60:
                                i-=1;
                                k+=1
                                valli.pop(j)
                                break
x=datetime.datetime.today()
y = x.replace(day=x.day, hour=21, minute=1, second=0, microsecond=0)
delta_t=y-x

secs=delta_t.total_seconds()

print(secs)
t = Timer(secs, teamform,args=['2020-05-21'])
t.start()
