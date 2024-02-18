from django.shortcuts import render
from django.http import HttpResponse
from .models import Speciality, Ensurance, Clinic
from django import forms
from .forms import SomeForm
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