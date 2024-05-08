from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Speciality, Ensurance, Clinic, Doctor, Dates, ClientDates, appUsers
from django import forms
from django.db import IntegrityError
from django.http import JsonResponse
import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


# Create your views here.


class createUser(forms.Form):
    user_name = forms.CharField(max_length=64)
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput(), min_length=8)
    email = forms.EmailField()


def index(request):
    request.session['dateVal'] = []
    return render(request, 'web/index.html')

def user(request):
    if request.user.is_authenticated:
        u = appUsers.objects.get(user = request.user)
        return render(request, 'web/user.html', {
            'dates': ClientDates.objects.filter(client=u),
            'u': u
            })
            
    else:
        return HttpResponseRedirect(reverse('signin'))

def signin(request):
    if request.method == 'POST':
        user_n = request.POST['user']
        passw = request.POST['password']
        user = authenticate(username=user_n, password=passw)
        if request.session['dateVal']:
            login(request, user)
            return HttpResponseRedirect(reverse('makedate', args=[request.session['dateVal'][0]]))
        if user != None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return HttpResponseRedirect(reverse('signin'))
        
    return render(request, 'web/signin.html')

def signup(request):
    form = createUser(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            user_name = form.cleaned_data['user_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirmation = form.cleaned_data['password2']

            if password != confirmation:
                 return render(request, 'web/signup.html', {
                    'message':'Passwords wont match',
                    'form':createUser()
                })
            
        try:
            user = User.objects.create_user(user_name, email, password)
            user.save()
            appuser = appUsers.objects.create(user=user)
            appuser.save()
            
        except IntegrityError:
            return render(request, 'web/signup.html', {
                    'message':'Username taken!',
                    'form':createUser()
                })
        if request.session['dateVal']:
            login(request, user)
            return HttpResponseRedirect(reverse('makedate', args=[request.session['dateVal'][0]]))
        else:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
    
    else:
        return render(request, 'web/signup.html', {
            'form': createUser()
        })

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def search(request):
    specialities = Speciality.objects.order_by('speciality')
    ensurance = Ensurance.objects.all()
    clinic = Clinic.objects.all()
    return render(request, "web/search.html",{
        'speciality':specialities,
        'ensurance':ensurance,
        'clinic':clinic
    })

def profile(request, doctor_id):
    doc = Doctor.objects.get(pk=doctor_id)
    return render(request, "web/profile.html", {
        'doctor': doc,
        'ens': doc.ensurance.all().values()
        })

def returnSearch(match, model):
    lista = []
    for p in model:
        p = p.serialize()
        if match == "''" or match == None:
            lista.append(p)
        elif match in p['name'].lower():
            lista.append(p)
    return(lista)

def doctor(request):
    speco = request.GET.get('speco')
    enseco = request.GET.get('enseco')
    clineco = request.GET.get('clineco')
    
    if speco != 'speciality':
        spec = Speciality.objects.get(pk = int(speco))
    else:
        spec = None

    if enseco != 'ensurance':
        ens = Ensurance.objects.get(pk = int(enseco))
    else:
        ens = None

    if clineco != 'clinic':
        clin = Clinic.objects.get(pk = int(clineco))
    else:
        clin = None

    pp =[]

    if spec != None and ens != None and clin != None:
        doctores = Doctor.objects.filter(speciality = spec, ensurance = ens, clinic = clin)
    elif spec and ens:
        doctores = Doctor.objects.filter(speciality = spec, ensurance = ens)    
    elif spec and clin:
        doctores = Doctor.objects.filter(speciality = spec, clinic = clin)
    elif ens and clin:
        doctores = Doctor.objects.filter(ensurance = ens, clinic = clin)
    elif spec:
        doctores = Doctor.objects.filter(speciality = spec)
    elif ens:
        doctores = Doctor.objects.filter(ensurance = ens)
    elif clin:
        doctores = Doctor.objects.filter(clinic = clin)
    else:
        doctores = Doctor.objects.all()


    for doc in doctores:
        doc = doc.serialize()
        pp.append(doc)

    return JsonResponse(pp, safe=False)

def ensurance(request, ens_id):
    return render(request, 'web/ensurance.html', {
        'ensurance': Ensurance.objects.get(pk=int(ens_id))
    })

def clinic(request, clin_name):
    return render(request, 'web/clinic.html', {
        'clinic': Clinic.objects.get(name=clin_name)
    })

def daysOn(request):
    user_id = request.GET.get('doctor')
    doctor = Doctor.objects.get(pk = user_id)
    horario = Dates.objects.filter(doctor = doctor)
    doc_schedule = []
    for h in horario:
        h = h.serialize()
        doc_schedule.append(h)

    if doc_schedule:  
        return JsonResponse(doc_schedule, safe=False)
    else:
        return JsonResponse(None, safe=False)
    
def docDates(request, doc_id):
    doc = Doctor.objects.get(pk=doc_id)
    dates = ClientDates.objects.filter(doctor=doc)
    dates_list = []
    for d in dates:
        d = d.serialize()
        dates_list.append(d)

    return JsonResponse(dates_list, safe=False)

weekdays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']


def makeDate(request, doc_id):
    doc = Doctor.objects.get(pk=doc_id)
    docdates = Dates.objects.filter(doctor=doc)
    if request.method =='POST':
        date = request.POST['date']
        clin = request.POST['clinic']
        clinic = Clinic.objects.get(name=clin)
            
        date = int(date)/1000 + 14400
        newdate = datetime.datetime.fromtimestamp(date)
        hours, min = newdate.strftime("%X")[:5].split(':')
        hours = int(hours) * 3600000
        min = int(min) * 60000

        if request.user.is_authenticated:
            try:
                u = appUsers.objects.get(user=request.user)

                # crear lista con los dias de la semana
                datesDays, takenDates, p = cDateArgs(docdates, doc, newdate, hours, min)

                # if the desired date day is not correct || 
                if p > len(datesDays) or date in takenDates:
                    return HttpResponse(f'NO ')
                else:  
                    ClientDates.objects.create(doctor=doc, clinic=clinic, date=newdate, client=u)
                    return HttpResponse(f'YES')
            except:
                return render(request, "web/profile.html", {
                    'doctor': doc,
                    'ens': doc.ensurance.all().values(),
                    'message': 'Unable to create the appointment'
                    })
        else:
            request.session['dateVal'] = [doc.id, clinic.id, date]   
            return render(request, 'web/signin.html', {
                'message': 'Unable to create the appointment!'
            })
    else:
        clinic = Clinic.objects.get(pk=int(request.session['dateVal'][1]))

        date = int(request.session['dateVal'][2])
        newdate = datetime.datetime.fromtimestamp(date)
        hours, min = newdate.strftime("%X")[:5].split(':')
        hours = int(hours) * 3600000
        min = int(min) * 60000

        datesDays, takenDates, p = cDateArgs(docdates, doc, newdate, hours, min)

        request.session['dateVal'] = []

        if p > len(datesDays) or date in takenDates:
            return HttpResponse(f'NO {newdate.strftime("%a")}{datesDays}{int(hours) + int(min) + 14400000}')
        else:  
            ClientDates.objects.create(doctor=doc, clinic=clinic, date=newdate, client=appUsers.objects.get(user=request.user))
            return HttpResponse(f'YES {newdate}')



def cDateArgs(docdates, doctor, nd, hours, min):
    datesDays=[]
    takenDates = []
    p = 0
    for d in docdates:
        t_datesLists = []
        for i in d.serialize()['days']:
            t_datesLists.append(weekdays[i - 1])
        datesDays.append(t_datesLists)


    for d in ClientDates.objects.filter(doctor=doctor):
        takenDates.append((int(d.serialize()['date'])/1000) + 14400)


    for d in range(len(datesDays) + 1):
        try:
            if nd.strftime("%a") in datesDays[d] and ((hours + min + 14400000) in docdates[d].serialize()['hours']):
                p = p
                break
            else:
                p+= 1 
        except IndexError:
            p = len(datesDays) + 2
    
    return datesDays, takenDates, p