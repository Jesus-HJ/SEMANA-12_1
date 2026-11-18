import re

from django import forms
from django.core.exceptions import ValidationError

from .models import Estudiante
from .validators import validar_apellido_o_nombre, validar_codigo_universitario


def sanitize_input(value, *, lowercase=False):
    """Normalize plain text; HTML escaping remains the template's job."""
    value = value.strip()
    return value.lower() if lowercase else value


class ContactoForm(forms.Form):
    correo = forms.EmailField(label="Correo electrónico")
    mensaje = forms.CharField(label="Mensaje", widget=forms.Textarea)

    def clean_correo(self):
        return sanitize_input(self.cleaned_data["correo"], lowercase=True)

    def clean_mensaje(self):
        return sanitize_input(self.cleaned_data["mensaje"])


class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = ("nombres", "apellidos", "codigo_universitario", "correo_electronico", "facultad", "carrera_profesional")
        labels = {
            "nombres": "Nombres",
            "apellidos": "Apellidos",
            "codigo_universitario": "Código universitario",
            "correo_electronico": "Correo electrónico",
            "facultad": "Facultad",
            "carrera_profesional": "Carrera profesional",
        }

    def clean_nombres(self):
        nombres = sanitize_input(self.cleaned_data["nombres"])
        if len(nombres) < 2:
            raise ValidationError("El nombre debe tener al menos 2 caracteres.")
        validar_apellido_o_nombre(nombres)
        return nombres

    def clean_apellidos(self):
        apellidos = sanitize_input(self.cleaned_data["apellidos"])
        if len(apellidos) < 2:
            raise ValidationError("Los apellidos deben tener al menos 2 caracteres.")
        validar_apellido_o_nombre(apellidos)
        return apellidos

    def clean_codigo_universitario(self):
        codigo = sanitize_input(self.cleaned_data["codigo_universitario"]).upper()
        validar_codigo_universitario(codigo)
        existentes = Estudiante.objects.filter(codigo_universitario=codigo)
        if self.instance.pk:
            existentes = existentes.exclude(pk=self.instance.pk)
        if existentes.exists():
            raise ValidationError("Ya existe un estudiante con ese código universitario.")
        return codigo

    def clean_correo_electronico(self):
        return sanitize_input(self.cleaned_data["correo_electronico"], lowercase=True)

    def clean_facultad(self):
        return sanitize_input(self.cleaned_data["facultad"])

    def clean_carrera_profesional(self):
        return sanitize_input(self.cleaned_data["carrera_profesional"])

    def clean(self):
        cleaned = super().clean()
        codigo = cleaned.get("codigo_universitario")
        correo = cleaned.get("correo_electronico")
        nombres = cleaned.get("nombres")
        apellidos = cleaned.get("apellidos")
        if codigo and correo and correo.partition("@")[0].casefold() == codigo.casefold():
            self.add_error("codigo_universitario", ValidationError(
                "El código no debe coincidir con el usuario del correo electrónico."
            ))
        if nombres and apellidos and nombres.casefold() == apellidos.casefold():
            raise ValidationError("Nombres y apellidos deben identificar partes distintas del nombre.")
        return cleaned
