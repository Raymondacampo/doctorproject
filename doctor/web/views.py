from django.shortcuts import render
from django.http import HttpResponse
from .models import Speciality, Ensurance, Clinic
from django import forms
from .forms import SomeForm
from django.http import JsonResponse

# Create your views here.

def index(request):
    specialities = Speciality.objects.all()
    ensurance = Ensurance.objects.all()
    clinic = Clinic.objects.all()
    return render(request, "web/index.html",{
        'specialities':specialities,
        'ensurance':ensurance,
        'clinic':clinic
    })

def search(request, doctor):
    return render(request, "web/index.html")



def returnSearch(tbvalue, model):
    lista = []
    for p in model:
        p = p.serialize()
        if tbvalue == "''" or tbvalue == None:
            lista.append(p)
        elif tbvalue in p['name'].lower():
            lista.append(p)
    return(lista)

def posibilities(request, model):
    match = request.GET.get('txt') or None
    
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
