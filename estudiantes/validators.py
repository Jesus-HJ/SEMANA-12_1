import re

from django.core.exceptions import ValidationError


NOMBRE_RE = re.compile(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+(?:[ '-][A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+)*")
CODIGO_RE = re.compile(r"\d{8}")


def validar_apellido_o_nombre(value):
    if not NOMBRE_RE.fullmatch(value):
        raise ValidationError("Usa letras; se permiten espacios, guiones y apóstrofes.")


def validar_codigo_universitario(value):
    if not CODIGO_RE.fullmatch(value):
        raise ValidationError("El código universitario debe contener exactamente 8 dígitos.")
