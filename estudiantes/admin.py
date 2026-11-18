from django.contrib import admin

from .models import Estudiante


@admin.action(description="Activar estudiantes seleccionados")
def activar_estudiantes(modeladmin, request, queryset):
    queryset.update(activo=True)


@admin.action(description="Desactivar estudiantes seleccionados")
def desactivar_estudiantes(modeladmin, request, queryset):
    queryset.update(activo=False)


@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ("codigo_universitario", "nombre_completo", "carrera_profesional", "activo", "fecha_registro")
    list_filter = ("activo", "facultad", "carrera_profesional")
    search_fields = ("nombres", "apellidos", "codigo_universitario", "correo_electronico")
    readonly_fields = ("fecha_registro",)
    fields = ("nombres", "apellidos", "codigo_universitario", "correo_electronico", "facultad", "carrera_profesional", "activo", "fecha_registro")
    actions = (activar_estudiantes, desactivar_estudiantes)

    @admin.display(description="Nombre completo", ordering="apellidos")
    def nombre_completo(self, obj):
        return f"{obj.nombres} {obj.apellidos}"
