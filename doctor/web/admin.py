from django.contrib import admin
from .models import Speciality, Clinic, Ensurance, Doctor
# Register your models here.
admin.site.register(Speciality)
admin.site.register(Clinic)
admin.site.register(Ensurance)
admin.site.register(Doctor)