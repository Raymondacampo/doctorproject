from django.db import models
from multiselectfield import MultiSelectField
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import datetime
# Create your models here.

# class User(AbstractUser):
#     pass

class Ensurance(models.Model):
    name = models.CharField(max_length=200)
    logo = models.URLField(blank=True)

    def __str__(self):
        return f"{self.name}"
    
    def serialize(self):
        return{
            'id':self.id,
            'name':f"{self.name}",
            'img':self.logo
        }

class User(AbstractUser):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, default=1,  related_name='appuser')
    email = models.EmailField(unique=True)
    profilePicture = models.URLField(default='https://i.imgflip.com/6yvpkj.jpg')
    ensurance = models.ManyToManyField(Ensurance, blank=True, related_name='appuser')
    def __str__(self) -> str:
        return f'{self.user}'
    


class Speciality(models.Model):
    speciality = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.speciality}"
    
    def serialize(self):
        return{
            'id':self.id,
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
            'id':self.id,
            'name':self.name
        }
    


class Doctor(models.Model):
    doctorUser = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, default=1,  related_name='doctor')
    speciality = models.ManyToManyField(Speciality, blank=True, related_name="doctors")
    clinic = models.ManyToManyField(Clinic, blank=True,  related_name="doctors")
    availability = models.CharField(max_length=500)
    contact = models.CharField(max_length=500)
    ensurance = models.ManyToManyField(Ensurance, related_name='doctors')
    image = models.URLField(default='https://i.imgflip.com/6yvpkj.jpg')
    description = models.CharField(max_length=400, blank=True)

    def __str__(self):
        return f"{self.doctorUser.name}"
    

    def serialize(self):
        return{
            'id':self.id,
            'name':self.doctorUser.name,
            'speciality':[f' {s.speciality}' for s in self.speciality.all()],
            'image':self.image,
            'clinic':[c.name for c in self.clinic.all()],
            'ensurance':[e.name for e in self.ensurance.all()],
            'logo':[e.logo for e in self.ensurance.all()]
        }
    
daysToPick = (
    ('SUN', 'Sunday'),
    ('MON', 'Monday'),
    ('TUE', 'Tuesday'),
    ('WED', 'Wednesday'),
    ('THU', 'Thursday'),
    ('FRI', 'Friday'),
    ('SAT', 'Saturday')
)

def toMil(val):
    return val * 3600000

hoursToPick = [
    (0, 0),
    (toMil(1), 1),
    (toMil(2), 2),
    (toMil(3), 3),
    (toMil(4), 4),
    (toMil(5), 5),
    (toMil(6), 6),
    (toMil(7), 7),
    (toMil(8), 8),
    (toMil(9), 9),
    (toMil(10), 10),
    (toMil(11), 11),
    (toMil(12), 12),
    (toMil(13), 13),
    (toMil(14), 14),
    (toMil(15), 15),
    (toMil(16), 16),
    (toMil(17), 17),
    (toMil(18), 18),
    (toMil(19), 19),
    (toMil(20), 20),
    (toMil(21), 21),
    (toMil(22), 22),
    (toMil(23), 23),
    (toMil(24), 24)
    ]



minToPick = [
    (0, 0),
    (int(toMil(0.5)), 30)
    ]
    


class Hours(models.Model):
    hora = models.IntegerField(choices=hoursToPick, default=00)
    minuto = models.IntegerField(choices=minToPick, default=00, blank=True)

    def __str__(self):
        if self.minuto != 0:
            return f'{int(self.hora/3600000)}:{int(self.minuto/60000)}'
        else:
            return f'{int(self.hora/3600000)}'

class Days(models.Model):
    dia = models.CharField(choices=daysToPick, max_length=300)

    def __str__(self):
        return f'{self.dia}'
    
class Dates(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete = models.CASCADE, related_name='dates')
    clinica = models.ForeignKey(Clinic, on_delete = models.CASCADE, default=0,related_name='dates')
    days = models.ManyToManyField(Days, related_name='dates')
    horas = models.ManyToManyField(Hours, related_name='dates')

    def __str__(self):
        return f'{self.doctor} Schedule in {self.clinica}'
    
    def serialize(self):
        return {
            'doctor': self.doctor.name,
            'clinic': self.clinica.name,
            'days': [d.id for d in self.days.all()],
            'hours': [(h.hora + h.minuto) for h in self.horas.all()],
            'strhours': [str(h) for h in self.horas.all()]
        }

class ClientDates(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete = models.CASCADE, default=1, related_name='clientDates')
    clinic = models.ForeignKey(Clinic, on_delete = models.CASCADE, default=1, related_name='clientDates')
    date = models.DateTimeField(default=datetime.datetime.now())
    client = models.ForeignKey(User, on_delete = models.CASCADE, default=1,  related_name='clientDates')
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.client} date with {self.doctor} on {self.date.strftime("%c")}'
    
    def img(self):
        return self.doctor.image
    
    def ren_date(self):
        return f'{self.date.strftime("%B")}-{self.date.strftime("%d")}-{self.date.strftime("%Y")}   {self.date.strftime("%X")[:5]}'

    def serialize(self):
        hm = self.date.strftime('%X')
        hours, minutes = hm[:-3].split(':')
        t_stamp = int(hours) * 3600000 + int(minutes) * 60000
        return {
            'doctor': self.doctor.name,
            'clinic':self.clinic.name,
            'client': self.client.user.username,
            'date': self.date.timestamp() * 1000,
            'time': t_stamp 
        }
    