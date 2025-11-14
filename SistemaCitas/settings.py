"""
Django settings for SistemaCitas project (versión adaptada para Render).
"""

import os
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv

# ============================
# 🔄 Cargar variables de entorno
# ============================

load_dotenv()  # carga variables desde .env localmente

# ============================
# 📁 Rutas base
# ============================

BASE_DIR = Path(__file__).resolve().parent.parent

# ============================
# 🔐 Seguridad
# ============================

SECRET_KEY = os.getenv("SECRET_KEY", "clave-insegura-local")
DEBUG = os.getenv("DEBUG", "True") == "True"

# Render define automáticamente RENDER_EXTERNAL_HOSTNAME
if not DEBUG:
    ALLOWED_HOSTS = [os.getenv("RENDER_EXTERNAL_HOSTNAME", "tudominio.com")]
else:
    ALLOWED_HOSTS = ["*"]

AUTH_USER_MODEL = 'core.Usuario'

# ============================
# 📦 Aplicaciones instaladas
# ============================

INSTALLED_APPS = [
    'gestion_citas',
    'core',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'widget_tweaks',
]

# ============================
# ⚙️ Middleware
# ============================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # para servir archivos estáticos
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'SistemaCitas.urls'

# ============================
# 🎨 Templates
# ============================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'SistemaCitas.wsgi.application'

# ============================
# 🗄️ Base de datos
# ============================

DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{os.path.join(BASE_DIR, 'db.sqlite3')}",  # SQLite local
        conn_max_age=600,
        ssl_require=not DEBUG  # SSL solo en producción
    )
}

# ============================
# 🔑 Validación de contraseñas
# ============================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ============================
# 🌍 Internacionalización
# ============================

LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/El_Salvador'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# ============================
# 📁 Archivos estáticos
# ============================

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'core', 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# WhiteNoise: sirve archivos estáticos comprimidos
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ============================
# 🚪 Redirecciones
# ============================

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

# ============================
# 🧱 Configuración por defecto
# ============================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

