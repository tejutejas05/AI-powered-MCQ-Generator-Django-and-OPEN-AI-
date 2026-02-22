from django.urls import path
from .views import generator_mcqs,home

urlpatterns = [
    path('',home,name="home"),
    path('generate/',generator_mcqs),
]