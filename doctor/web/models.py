from django.db import models

# Create your models here.

class Ensurance(models.Model):
    name = models.CharField(max_length=200)
    plan = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name}, {self.plan}."
    
    def serialize(self):
        return{
            'name':self.name
        }

class Speciality(models.Model):
    speciality = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.speciality}"
    
    def serialize(self):
        return{
            'name':self.speciality
        }

class Clinic(models.Model):
    name = models.CharField(max_length=200)
    adress = models.CharField(max_length=500)
    ensurance = models.ManyToManyField(Ensurance, blank=True, related_name="clinics")
    contact = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"
    
    def serialize(self):
        return{
            'name':self.name
        }

class Doctor(models.Model):
    name = models.CharField(max_length=200)
    speciality = models.ManyToManyField(Speciality, related_name="doctors")
    clinic = models.ManyToManyField(Clinic, blank=True,  related_name="doctors")
    availability = models.CharField(max_length=500)
    contact = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.name}"