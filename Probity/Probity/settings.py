"""
Django settings for Probity project.
"""

from pathlib import Path
import os
import dj_database_url  # <--- Importado para la configuración de la base de datos
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Cargar variables de entorno desde .env (principalmente para desarrollo local)
load_dotenv(BASE_DIR / ".env")

# --- Claves Secretas y Configuraciones de Entorno ---

# SECURITY WARNING: keep the secret key used in production secret!
# Lee la SECRET_KEY desde las variables de entorno. Nunca la dejes hardcodeada.
SECRET_KEY = os.getenv("SECRET_KEY", 'django-insecure-a1=(7c10+#g8d=40uj%h0o4&lfadwz1=0q)(nu0v2$4a4m&fp8')

# GEMINI API KEY
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG se desactivará automáticamente en Render (cuando la variable 'RENDER' exista)
DEBUG = 'RENDER' not in os.environ

# Configuración de los hosts permitidos para producción
ALLOWED_HOSTS = []
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.formulas.apps.FormulasConfig',
    'apps.chatbot',
    'rest_framework',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # <--- Añadido para servir archivos estáticos
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware', # <--- Movido para que esté después de Security y WhiteNoise
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# --- Configuración de CORS para Producción ---
# En producción, solo permitiremos la URL de nuestro frontend desplegado
# Vercel te dará una URL como "https://mi-proyecto.vercel.app"

CORS_ALLOWED_ORIGINS = [
    # Para desarrollo local
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
# Lee la URL del frontend desplegado desde una variable de entorno
FRONTEND_URL = os.getenv('FRONTEND_URL')
if FRONTEND_URL:
    CORS_ALLOWED_ORIGINS.append(FRONTEND_URL)


ROOT_URLCONF = 'Probity.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'Probity.wsgi.application'


# --- Base de Datos para Producción ---
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(
        # Render te dará la variable DATABASE_URL. Si no existe, usa SQLite.
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600
    )
}


# Password validation
# ... (sin cambios aquí) ...

AUTH_PASSWORD_VALIDATORS = [
    # ...
]

# Internationalization
# ... (sin cambios aquí) ...

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# --- Archivos Estáticos para Producción ---
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# Esta configuración se activa solo cuando DEBUG es False (en producción)
if not DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# ... (sin cambios aquí) ...
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'