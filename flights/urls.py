from django.urls import path
from . import views

app_name = "flights"
urlpatterns = [
     path('', views.index, name="index"),
     path("<str:flight_id>", views.flight, name="flight"),
     path("<str:flight_id>/book", views.book, name="book")
]