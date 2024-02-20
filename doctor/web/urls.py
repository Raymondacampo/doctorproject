from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search/<str:doctor>", views.search, name="search"),

    path("posibilities/<str:model>", views.posibilities, name="posibilities")
]