import os
from pathlib import Path
from django.conf import settings
import environ
import dj_database_url

# --- ENV / BASE_DIR ---
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
# OJO: environ.Env.read_env() sin argumentos busca el .env junto a este
# settings.py (fye_site/fye_site/), NO junto a manage.py (fye_site/). El
# .env real del proyecto vive junto a manage.py, por eso se indica la ruta
# explicita a BASE_DIR/.env.
environ.Env.read_env(str(BASE_DIR / ".env"))

# --- CORE ---
SECRET_KEY = env("SECRET_KEY", default="dev-secret")
DEBUG = env.bool("DEBUG", default=True)

# ALLOWED_HOSTS: lista separada por comas en la variable de entorno, ej:
# ALLOWED_HOSTS=tu-app.onrender.com,www.tu-app.onrender.com
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])

ROOT_URLCONF = 'fye_site.urls'  # <- ajusta al nombre real del paquete del proyecto


# --- APPS ---
INSTALLED_APPS = [
    # Django

    # ...
    "miembros.apps.MiembrosConfig",
    # ...
    "django_extensions",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",  # requerido por allauth
    

    # Terceros
    "allauth",
    "allauth.account",
    "allauth.socialaccount",  # opcional
    "guardian",               # permisos por objeto
    "widget_tweaks",        # para personalizar widgets en templates

    # Tus apps
    "accounts",
    "rls",
    #"miembros",
    "meetings",
    "finance",
    "mediax",
    "auditlog",
    "dashboard",
]

# --- AUTH ---
AUTH_USER_MODEL = "accounts.User"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",                    # auth base
    "allauth.account.auth_backends.AuthenticationBackend",         # allauth
    "guardian.backends.ObjectPermissionBackend",                   # guardian (opcional pero útil)
]

SITE_ID = 1

# Rutas de login/logout
LOGIN_URL = "account_login"
LOGIN_REDIRECT_URL = "dashboard:home"   # usa "/" si aún no tienes esa URL nombrada
LOGOUT_REDIRECT_URL = "/"

# --- MIDDLEWARE ---
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # sirve los estáticos en producción
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "allauth.account.middleware.AccountMiddleware",  # requerido por allauth
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# --- TEMPLATES ---
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",  # requerido por allauth
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# --- STATIC & MEDIA ---
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]     # asegúrate de crear BASE_DIR/static
STATIC_ROOT = BASE_DIR / "staticfiles"       # para collectstatic en producción

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}

# --- DATABASE (PostgreSQL) ---
# Si existe DATABASE_URL en el entorno (Render la inyecta sola al conectar
# la base de datos al Web Service), se usa esa. Si no, cae a las variables
# PG* de siempre (tu .env local).
DATABASES = {
    "default": dj_database_url.config(
        default=(
            f"postgresql://{env('PGUSER', default='fye_user')}:"
            f"{env('PGPASSWORD', default='')}@"
            f"{env('PGHOST', default='127.0.0.1')}:"
            f"{env('PGPORT', default='5432')}/"
            f"{env('PGDATABASE', default='fye')}"
        ),
        conn_max_age=60,
    )
}
DATABASES["default"]["OPTIONS"] = {"connect_timeout": 5}

# --- ALLAUTH (config moderna sin deprecations) ---
# Si tu User NO tiene campo username (modelo por email), deja esto en None.
# Si tu User SÍ conserva username, elimina esta línea.
ACCOUNT_USER_MODEL_USERNAME_FIELD = None

# Métodos de inicio de sesión permitidos (set):
# {"email"} para solo email; {"username"}, o {"username", "email"} si quieres ambos.
ACCOUNT_LOGIN_METHODS = {"email"}

# Campos del signup y requeridos (marcados con '*')
ACCOUNT_SIGNUP_FIELDS = ["email*", "password1*", "password2*"]

# Verificación de email (ajusta a "mandatory" si vas a enviar correos reales)
ACCOUNT_EMAIL_VERIFICATION = "none"

# --- EMAIL (para "olvide mi contrasena" y notificaciones) ---
# Si defines EMAIL_HOST en el .env se envian correos reales por SMTP.
# Si se deja vacio, se usa el backend de consola: los correos solo se
# imprimen en la terminal (sirve para desarrollo, nadie los recibe de verdad).
EMAIL_HOST = env("EMAIL_HOST", default="")
if EMAIL_HOST:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_PORT = env.int("EMAIL_PORT", default=587)
    EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
    EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")
    EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=True)
    EMAIL_USE_SSL = env.bool("EMAIL_USE_SSL", default=False)
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

DEFAULT_FROM_EMAIL = env(
    "DEFAULT_FROM_EMAIL", default="Fe y Esperanza No. 1 <no-reply@feyesperanza.org>"
)

# --- GUARDIAN ---
ANONYMOUS_USER_NAME = "anonymous"

# --- I18N / TZ ---
LANGUAGE_CODE = "es-mx"
TIME_ZONE = "America/Monterrey"
USE_I18N = True
USE_TZ = True

# --- SECURITY (ajustadas por DEBUG) ---
SECURE_SSL_REDIRECT = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG

# CSRF_TRUSTED_ORIGINS: lista separada por comas en la variable de entorno, ej:
# CSRF_TRUSTED_ORIGINS=https://tu-app.onrender.com
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[])

#SECRET_KEY=dev-secret
#DEBUG=True

#PGDATABASE=fye
#PGUSER=postgres
#PGPASSWORD=postgres
#PGHOST=127.0.0.1
#PGPORT=5432

#ALLOWED_HOSTS=localhost,127.0.0.1
#CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
