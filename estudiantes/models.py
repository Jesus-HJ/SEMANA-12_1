from django.db import models

from .validators import validar_apellido_o_nombre, validar_codigo_universitario


class Estudiante(models.Model):
    nombres = models.CharField(max_length=80, validators=[validar_apellido_o_nombre])
    apellidos = models.CharField(max_length=100, validators=[validar_apellido_o_nombre])
    codigo_universitario = models.CharField(max_length=12, unique=True, validators=[validar_codigo_universitario])
    correo_electronico = models.EmailField(max_length=254)
    facultad = models.CharField(max_length=120)
    carrera_profesional = models.CharField(max_length=120)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ["apellidos", "nombres"]
        verbose_name = "estudiante"
        verbose_name_plural = "estudiantes"

    def __str__(self):
        return f"{self.apellidos}, {self.nombres} ({self.codigo_universitario})"
