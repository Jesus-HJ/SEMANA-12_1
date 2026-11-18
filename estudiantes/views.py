from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.html import escape
from django.views.generic import ListView

from .forms import ContactoForm, EstudianteForm
from .models import Estudiante


def inicio(request):
    return render(request, "inicio.html")


def registrar_estudiante(request):
    form = EstudianteForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "El registro del estudiante se completó correctamente.")
        return redirect("estudiantes:lista")
    return render(request, "registro.html", {"form": form})


class ListaEstudiantesView(PermissionRequiredMixin, ListView):
    model = Estudiante
    template_name = "lista_estudiantes.html"
    context_object_name = "estudiantes"
    permission_required = "estudiantes.view_estudiante"
    # IA: el primer ajuste respondió 403 también a visitantes → conservar el
    # comportamiento de AccessMixin: anónimos al login y usuarios sin permiso 403.

    def get_queryset(self):
        return Estudiante.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["puede_ver_estudiantes"] = self.request.user.has_perm("estudiantes.view_estudiante")
        return context


lista_estudiantes = ListaEstudiantesView.as_view()


def contacto(request):
    form = ContactoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        # Ejemplo de Form clásico: los datos validados no se almacenan.
        mensaje = form.cleaned_data["mensaje"]
        # escape() se aplica solo a la salida mostrada; el texto persistido no se modifica.
        return render(request, "contacto.html", {"form": ContactoForm(), "enviado": True, "mensaje": escape(mensaje)})
    return render(request, "contacto.html", {"form": form})
