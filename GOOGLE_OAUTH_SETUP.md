# Configuración de Google OAuth

## Paso 1: Crear proyecto en Google Cloud Console

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuevo proyecto o selecciona uno existente
3. En el menú lateral, ve a "APIs y servicios" > "Credenciales"

## Paso 2: Configurar pantalla de consentimiento OAuth

1. Haz clic en "Pantalla de consentimiento de OAuth"
2. Selecciona "Externo" y haz clic en "Crear"
3. Completa la información básica:
   - Nombre de la aplicación: **Pichanga Manager**
   - Correo de asistencia al usuario: tu email
   - Correo de contacto del desarrollador: tu email
4. Guarda y continúa

## Paso 3: Crear credenciales OAuth 2.0

1. Ve a "Credenciales" > "Crear credenciales" > "ID de cliente de OAuth 2.0"
2. Tipo de aplicación: **Aplicación web**
3. Nombre: **Pichanga Manager Web**
4. Orígenes de JavaScript autorizados:
   - `https://pichanga-manager-demo.fly.dev`
5. URIs de redireccionamiento autorizadas:
   - `https://pichanga-manager-demo.fly.dev/accounts/google/login/callback/`
6. Haz clic en "Crear"
7. **Guarda el Client ID y el Client Secret**

## Paso 4: Configurar en la aplicación Django

### Opción A: Usando el Admin de Django

1. Ve a https://pichanga-manager-demo.fly.dev/admin/
2. Inicia sesión como superusuario (si no tienes uno, créalo con el comando de abajo)
3. Ve a "Sites" y asegúrate de que el site sea: `pichanga-manager-demo.fly.dev`
4. Ve a "Social applications" > "Add social application"
5. Completa:
   - Provider: **Google**
   - Name: **Google**
   - Client id: (el que copiaste)
   - Secret key: (el que copiaste)
   - Sites: selecciona `pichanga-manager-demo.fly.dev`
6. Guarda

### Opción B: Usando el shell de Django

```bash
flyctl ssh console -a pichanga-manager-demo -C "python /app/manage.py shell"
```

```python
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

# Crear o actualizar el site
site = Site.objects.get(pk=1)
site.domain = 'pichanga-manager-demo.fly.dev'
site.name = 'Pichanga Manager'
site.save()

# Crear la aplicación social de Google
google_app = SocialApp.objects.create(
    provider='google',
    name='Google',
    client_id='TU_CLIENT_ID_AQUI',
    secret='TU_CLIENT_SECRET_AQUI'
)
google_app.sites.add(site)
google_app.save()

print("✅ Configuración de Google OAuth completada!")
```

## Paso 5: Crear superusuario (si no existe)

```bash
flyctl ssh console -a pichanga-manager-demo -C "python /app/manage.py createsuperuser"
```

## Paso 6: Habilitar el botón de Google

Una vez configurado, descomenta las secciones de Google OAuth en:
- `templates/account/login.html`
- `templates/account/signup.html`

Y haz deploy de nuevo:
```bash
flyctl deploy --ha=false
```

## Verificar que funciona

1. Ve a https://pichanga-manager-demo.fly.dev/accounts/login/
2. Haz clic en "Google"
3. Deberías ser redirigido a Google para autenticarte
4. Después de aprobar, volverás a la aplicación ya autenticado

## Troubleshooting

### Error: redirect_uri_mismatch
- Verifica que la URL de redirección en Google Cloud Console sea exactamente:
  `https://pichanga-manager-demo.fly.dev/accounts/google/login/callback/`

### Error: SocialApp matching query does not exist
- Asegúrate de haber creado la SocialApp en el admin o con el shell

### Error: Site matching query does not exist
- Verifica que el SITE_ID en settings.py coincida con el site en la base de datos
