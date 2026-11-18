from django.urls import path

from . import views

app_name = "estudiantes"

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("registro/", views.registrar_estudiante, name="registro"),
    path("estudiantes/", views.lista_estudiantes, name="lista"),
    path("contacto/", views.contacto, name="contacto"),
]
