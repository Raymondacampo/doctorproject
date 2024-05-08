from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("myuser", views.user, name='user'),
    path("signin", views.signin, name='signin'),
    path("signup", views.signup, name='signup'),
    path('logout', views.logout_view, name="logout"),
    path("search", views.search, name="search"),
    path("<int:doctor_id>/profile", views.profile, name="profile"),
    path("makedate/<int:doc_id>", views.makeDate, name='makedate'),
    path('doctor', views.doctor, name='doctor'),
    path('dayson', views.daysOn, name='dayson'),
    path("docdates/<int:doc_id>", views.docDates, name="docdates"),
    path('ensurance/<int:ens_id>', views.ensurance, name='ensurance'),
    path('clinic/<str:clin_name>', views.clinic, name='clinic'),
]