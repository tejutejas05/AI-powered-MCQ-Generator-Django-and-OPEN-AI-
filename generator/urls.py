from django.urls import path
from .views import generator_mcqs

urlpatterns = [
    path('generate/',generator_mcqs),
]