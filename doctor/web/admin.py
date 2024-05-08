from django.contrib import admin
from .models import Speciality, Clinic, Ensurance, Doctor, Days, Hours, Dates, ClientDates, appUsers
# Register your models here.

admin.site.register(Speciality)
admin.site.register(Clinic)
admin.site.register(Ensurance)
admin.site.register(Doctor)
admin.site.register(Days)
admin.site.register(Hours)
admin.site.register(Dates)
admin.site.register(ClientDates)
admin.site.register(appUsers)