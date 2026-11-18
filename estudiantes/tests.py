import logging
import secrets

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import Client, TestCase
from django.urls import reverse

from .admin import activar_estudiantes, desactivar_estudiantes
from .forms import ContactoForm, EstudianteForm
from .models import Estudiante


class EstudianteFormTests(TestCase):
    def payload(self, **updates):
        data = {
            "nombres": " Ana María ",
            "apellidos": "Pérez-García",
            "codigo_universitario": "20260001",
            "correo_electronico": " ANA@Example.EDU ",
            "facultad": " Sistemas ",
            "carrera_profesional": " Ingeniería de Sistemas ",
        }
        data.update(updates)
        return data

    def test_valid_form_normalizes_input(self):
        form = EstudianteForm(data=self.payload())
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["nombres"], "Ana María")
        self.assertEqual(form.cleaned_data["correo_electronico"], "ana@example.edu")
        estudiante = form.save()
        self.assertEqual(Estudiante.objects.get(pk=estudiante.pk).codigo_universitario, "20260001")

    def test_empty_fields_rejected(self):
        form = EstudianteForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn("nombres", form.errors)
        self.assertIn("correo_electronico", form.errors)

    def test_invalid_names_and_surnames_rejected(self):
        for field, value in (("nombres", "Ana2"), ("apellidos", "Pérez@")):
            with self.subTest(field=field):
                form = EstudianteForm(data=self.payload(**{field: value}))
                self.assertFalse(form.is_valid())
                self.assertIn(field, form.errors)

    def test_code_format_and_duplicate_rejected(self):
        form = EstudianteForm(data=self.payload(codigo_universitario="ABC"))
        self.assertFalse(form.is_valid())
        self.assertIn("codigo_universitario", form.errors)
        Estudiante.objects.create(**{
            "nombres": "Lucía", "apellidos": "Quispe", "codigo_universitario": "20260002",
            "correo_electronico": "lucia@example.edu", "facultad": "Sistemas",
            "carrera_profesional": "Informática",
        })
        duplicate = EstudianteForm(data=self.payload(codigo_universitario=" 20260002 "))
        self.assertFalse(duplicate.is_valid())
        self.assertIn("codigo_universitario", duplicate.errors)

    def test_invalid_email_and_cross_field_rules(self):
        invalid_email = EstudianteForm(data=self.payload(correo_electronico="no-es-correo"))
        self.assertFalse(invalid_email.is_valid())
        self.assertIn("correo_electronico", invalid_email.errors)
        duplicate_identity = EstudianteForm(data=self.payload(nombres="Ana", apellidos="Ana"))
        self.assertFalse(duplicate_identity.is_valid())
        self.assertIn("__all__", duplicate_identity.errors)
        code_email = EstudianteForm(data=self.payload(correo_electronico="20260001@example.edu"))
        self.assertFalse(code_email.is_valid())
        self.assertIn("codigo_universitario", code_email.errors)

    def test_contact_form_sanitizes_whitespace(self):
        form = ContactoForm(data={"correo": " USER@EXAMPLE.EDU ", "mensaje": "  Hola  "})
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["correo"], "user@example.edu")
        self.assertEqual(form.cleaned_data["mensaje"], "Hola")


class WebFlowTests(TestCase):
    def setUp(self):
        self.user_model = get_user_model()
        self.user_password = secrets.token_urlsafe(24)
        self.admin_password = secrets.token_urlsafe(24)
        self.user = self.user_model.objects.create_user(username="alumno", password=self.user_password)
        self.admin = self.user_model.objects.create_superuser(username="admin", email="admin@example.edu", password=self.admin_password)
        self.payload = {
            "nombres": "Mario", "apellidos": "Rojas", "codigo_universitario": "20261111",
            "correo_electronico": "mario@example.edu", "facultad": "Sistemas",
            "carrera_profesional": "Computación",
        }

    def test_registration_get_and_successful_post(self):
        self.assertEqual(self.client.get(reverse("estudiantes:registro")).status_code, 200)
        response = self.client.post(reverse("estudiantes:registro"), self.payload, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.redirect_chain)
        self.assertContains(response, "El registro del estudiante se completó correctamente.")
        self.assertTrue(Estudiante.objects.filter(codigo_universitario="20261111").exists())

    def test_contact_output_is_escaped_without_storing_html(self):
        response = self.client.post(reverse("estudiantes:contacto"), {
            "correo": "alumno@example.edu", "mensaje": "<script>alert(1)</script>",
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "&lt;script&gt;alert(1)&lt;/script&gt;")
        self.assertNotContains(response, "<script>alert(1)</script>")

    def test_csrf_rejects_post_without_token(self):
        client = Client(enforce_csrf_checks=True)
        response = client.post(reverse("estudiantes:registro"), self.payload)
        self.assertEqual(response.status_code, 403)
        form_page = client.get(reverse("estudiantes:registro"))
        self.assertEqual(form_page.status_code, 200)
        csrf_token = client.cookies["csrftoken"].value
        response = client.post(reverse("estudiantes:registro"), {
            **self.payload, "csrfmiddlewaretoken": csrf_token,
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Estudiante.objects.filter(codigo_universitario="20261111").exists())

    def test_login_and_permission_restriction(self):
        target = reverse("estudiantes:lista")
        response = self.client.get(target)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)
        self.assertEqual(self.client.post(reverse("login"), {"username": "alumno", "password": secrets.token_urlsafe(18)}).status_code, 200)
        self.assertTrue(self.client.login(username="alumno", password=self.user_password))
        self.assertEqual(self.client.get(target).status_code, 403)
        permission = Permission.objects.get(codename="view_estudiante", content_type__app_label="estudiantes")
        self.user.user_permissions.add(permission)
        self.assertEqual(self.client.get(target).status_code, 200)
        logout_response = self.client.post(reverse("logout"))
        self.assertEqual(logout_response.status_code, 302)
        self.assertEqual(self.client.get(target).status_code, 302)

    def test_complete_registration_login_restricted_admin_logout_flow(self):
        target = reverse("estudiantes:lista")
        registration = self.client.post(reverse("estudiantes:registro"), self.payload)
        self.assertEqual(registration.status_code, 302)
        self.assertEqual(registration.url, target)
        self.assertEqual(self.client.get(target).status_code, 302)

        permission = Permission.objects.get(codename="view_estudiante", content_type__app_label="estudiantes")
        self.user.user_permissions.add(permission)
        self.user.is_staff = True
        self.user.save(update_fields=["is_staff"])
        login = self.client.post(reverse("login"), {"username": "alumno", "password": self.user_password})
        self.assertEqual(login.status_code, 302)
        self.assertEqual(self.client.get(target).status_code, 200)
        self.assertEqual(self.client.get(reverse("admin:estudiantes_estudiante_changelist")).status_code, 200)
        self.assertEqual(self.client.post(reverse("logout")).status_code, 302)
        self.assertEqual(self.client.get(target).status_code, 302)

    def test_logout_requires_csrf_with_enforced_client(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.admin)
        self.assertEqual(client.post(reverse("logout")).status_code, 403)
        client.get(reverse("login"))
        token = client.cookies["csrftoken"].value
        response = client.post(reverse("logout"), {"csrfmiddlewaretoken": token})
        self.assertEqual(response.status_code, 302)

    def test_admin_authentication_search_filter_and_actions(self):
        student = Estudiante.objects.create(**self.payload)
        changelist = reverse("admin:estudiantes_estudiante_changelist")
        self.assertEqual(self.client.get(changelist).status_code, 302)
        self.client.force_login(self.admin)
        response = self.client.get(changelist, {"q": "20261111", "activo__exact": "1"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Mario Rojas")
        activar_estudiantes(None, None, Estudiante.objects.filter(pk=student.pk))
        student.refresh_from_db()
        self.assertTrue(student.activo)
        desactivar_estudiantes(None, None, Estudiante.objects.filter(pk=student.pk))
        student.refresh_from_db()
        self.assertFalse(student.activo)

    def test_middleware_csp_security_and_session_cookie(self):
        with self.assertLogs("estudiantes.audit", level=logging.INFO) as captured:
            response = self.client.get(reverse("estudiantes:inicio"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["X-Frame-Options"], "DENY")
        self.assertIn("Content-Security-Policy", response)
        self.assertTrue(any("GET / -> 200" in line for line in captured.output))
        self.client.get(reverse("login"))
        self.assertIn("csrftoken", self.client.cookies)
        login_response = self.client.post(reverse("login"), {"username": "alumno", "password": self.user_password})
        self.assertIn("sessionid", login_response.cookies)
        self.assertTrue(login_response.cookies["sessionid"]["httponly"])
        self.assertEqual(login_response.cookies["sessionid"]["samesite"], "Lax")
        self.assertFalse(login_response.cookies["sessionid"]["secure"])

