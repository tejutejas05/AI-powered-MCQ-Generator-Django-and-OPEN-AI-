from django.urls import path
from .views import generator_mcqs,home,download_pdf

urlpatterns = [
    path('',home,name="home"),
    path('generate/',generator_mcqs),
    path('download/',download_pdf, name='download_pdf'),
]