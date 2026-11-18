# Sistema de Registro de Estudiantes

Práctica IS093A, Semana 12. Proyecto académico desarrollado con Python 3.11, Django 5.2.19 y SQLite.

## Instalación local en Windows

```powershell
py -3.11 -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Abre `http://127.0.0.1:8000/`. El panel Admin está en `/admin/`. Si PowerShell bloquea la activación del entorno, solo para esa sesión ejecuta `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` y vuelve a activar `venv`.

## Funcionalidades

- Inicio, formulario `forms.Form` de contacto y registro de estudiantes con `ModelForm`.
- Validación de nombres, apellidos, código de ocho dígitos, email, duplicados y reglas cruzadas; normalización de espacios y email.
- Persistencia SQLite con validadores y unicidad en el modelo.
- Admin con nombre calculado, búsqueda, filtros y acciones masivas para activar/desactivar.
- Inicio/cierre de sesión, protección CSRF, lista con permiso `estudiantes.view_estudiante`.
- Middleware con registro de método/ruta/estado y encabezados CSP; `X-Frame-Options: DENY`.

Para habilitar el listado a un usuario, asigna `estudiantes.view_estudiante` desde Admin. Para usar el Admin, la cuenta debe ser `is_staff` (un superusuario ya lo es).

## Comprobaciones

Desde la raíz del proyecto, con `venv` activado:

```powershell
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
python manage.py check --deploy
```

El perfil local usa HTTP y `DEBUG=True`; por eso `check --deploy` informa advertencias de producción. No desactives las protecciones para ocultarlas. Antes de servir por HTTPS, define variables de entorno en el entorno del servidor. Ejemplo PowerShell (no guardes la clave en archivos versionados):

```powershell
$env:DJANGO_DEBUG = "0"
$env:DJANGO_SECRET_KEY = "<clave aleatoria secreta generada para el despliegue>"
$env:DJANGO_ALLOWED_HOSTS = "tu-dominio.edu"
$env:DJANGO_HTTPS = "1"
```

`DJANGO_HTTPS=1` activa cookies `Secure`, redirección HTTPS y HSTS. Configura y verifica HTTPS en el servidor/proxy antes de usarlo. `requirements.txt` declara Django; no se requieren dependencias adicionales para ejecutar el proyecto.

## Evidencias y estado académico

Las capturas reales, sus descripciones y el informe de verificación están en `evidencias/` e `INFORME_PRACTICA.md`. Se usó asistencia de IA para implementar y revisar código. Por ello no se acredita que el estudiante haya escrito manualmente el 80 % de validación, middleware y seguridad. Consulta `PENDIENTES_MANUALES.md` y confirma con el docente cómo cumplir esa condición académica; no presentes código generado como trabajo manual propio.

## Preparación para GitHub

El repositorio local ya está inicializado. Revisa antes de publicar:

```powershell
git status --short
git add .
git diff --cached --stat
git diff --cached
git commit -m "Completa práctica Django Semana 12"
git remote add origin <URL-del-repositorio>
git push -u origin main
```

Los comandos de commit y publicación son instrucciones; no se hizo `git push`. `.gitignore` excluye entorno virtual, base SQLite local, `.env`, cachés y archivos temporales del navegador. No agregues claves, contraseñas ni datos privados.
