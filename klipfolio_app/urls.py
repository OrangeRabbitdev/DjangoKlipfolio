from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('generar-pdf/', views.generar_pdf, name='generar_pdf'),
]