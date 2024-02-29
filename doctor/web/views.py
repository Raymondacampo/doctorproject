from django.shortcuts import render
from django.http import HttpResponse
from .models import Speciality, Ensurance, Clinic, Doctor
from django import forms
from .forms import SomeForm
from django.http import JsonResponse

# Create your views here.

def index(request):
    specialities = Speciality.objects.order_by('speciality')
    ensurance = Ensurance.objects.all()
    clinic = Clinic.objects.all()
    return render(request, "web/index.html",{
        'speciality':specialities,
        'ensurance':ensurance,
        'clinic':clinic
    })

def search(request, doctor):
    return render(request, "web/index.html")



def returnSearch(match, model):
    lista = []
    for p in model:
        p = p.serialize()
        if match == "''" or match == None:
            lista.append(p)
        elif match in p['name'].lower():
            lista.append(p)
    return(lista)

def posibilities(request, model):
    match = request.GET.get('match') or None
    
    if model == 'speciality':
        obj = Speciality.objects.all()
        oo = returnSearch(match, obj)
        return JsonResponse(oo, safe=False)
    
    elif model == 'ensurance':
        obj = Ensurance.objects.all()
        oo = returnSearch(match, obj)
        return JsonResponse(oo, safe=False)
    
    elif model == 'clinic':
        obj =  Clinic.objects.all()
        oo = returnSearch(match, obj)
        return JsonResponse(oo, safe=False)



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
        doctores = 'popolon'


    for doc in doctores:
        doc = doc.serialize()
        pp.append(doc)

    return JsonResponse(pp, safe=False)