# Evidencias — Práctica Semana 12

Las capturas son imágenes reales generadas con el navegador local. Se usaron datos ficticios. El registro de la lista protegida está enmascarado para no exponer contenido preexistente de SQLite; las capturas de Admin filtran el código ficticio de evidencia. Los usuarios/estudiantes temporales se eliminaron tras capturar.

| Archivo | Evidencia |
|---|---|
| `01_inicio.png` | Página principal |
| `02_errores_registro_vacio.png` | Validación de envío vacío |
| `03_login_admin.png` | Login requerido para Admin |
| `04_admin_inicio.png` | Inicio de Admin autenticado |
| `05_admin_estudiantes.png` | Búsqueda Admin filtrada por código ficticio |
| `06_formulario_estudiante.png` | Formulario de registro |
| `07_validaciones_nombre_apellido.png` | Rechazo de nombres/apellidos con caracteres inválidos |
| `08_codigo_universitario_invalido.png` | Rechazo de formato de código inválido |
| `09_codigo_duplicado.png` | Rechazo de código universitario existente |
| `10_registro_exitoso.png` | Registro aceptado y mensaje de éxito; luego se solicita login para lista restringida |
| `11_inicio_sesion.png` | Formulario de inicio de sesión |
| `12_acceso_sin_sesion.png` | Redirección al login al intentar abrir el listado sin sesión |
| `13_acceso_con_permiso.png` | Listado accesible con permiso; celdas ocultas para privacidad |
| `14_cierre_sesion.png` | Inicio después de cerrar sesión |
| `15_panel_administracion.png` | Panel Admin autenticado |
| `16_busqueda_filtro_admin.png` | Admin con búsqueda y filtro de estado |
| `17_accion_masiva_seleccionada.png` | Acción desactivar seleccionada para registro ficticio |
| `18_resultado_accion_desactivar.png` | Registro ficticio tras aplicar desactivación |
| `19_accion_masiva_aplicada.png` | Filtro “activo” ya no encuentra el registro desactivado |
| `20_pruebas_automatizadas.png` | Salida de las pruebas Django renderizada para captura |
| `20_resultado_pruebas.txt` | Salida de consola capturada directamente de `manage.py test` |
| `21_middleware_y_seguridad.png` | Extractos de configuración/middleware leídos de los archivos actuales |

Las capturas de configuración y pruebas se prepararon con una página temporal que mostró el contenido de los archivos/salida reales y luego se retiró. La página no forma parte del sistema entregable.

## Para capturas adicionales

1. Ejecuta `python manage.py runserver` y abre `http://127.0.0.1:8000/`.
2. No captures valores de cookies, contraseñas, claves ni registros privados.
3. En DevTools, captura solo nombres/atributos de cookies y encabezados si la entrega requiere evidencia visual específica de cookies, CSP y `X-Frame-Options`.
4. `Secure=False` es correcto en HTTP local; para HTTPS de producción se debe activar `DJANGO_HTTPS=1`.
