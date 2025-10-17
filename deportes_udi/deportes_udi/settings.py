from pathlib import Path

# BASE_DIR: ruta base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# =====================================================
# CONFIGURACIONES GENERALES
# =====================================================
SECRET_KEY = 'django-insecure-pon-aqui-tu-clave-secreta'
DEBUG = True
ALLOWED_HOSTS = []

# =====================================================
#  APLICACIONES INSTALADAS
# =====================================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'eventos',  # <-- Tu aplicación
]

# =====================================================
# MIDDLEWARE
# =====================================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# =====================================================

# =====================================================
ROOT_URLCONF = 'deportes_udi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'eventos' / 'templates'],  # Plantillas personalizadas
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'deportes_udi.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'deportes_udi_db',  
        'USER': 'root',              
        'PASSWORD': '',              
        'HOST': 'localhost',
        'PORT': '3307',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# =====================================================
#  ZONA HORARIA Y LENGUAJE
# =====================================================
LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_TZ = True

# =====================================================
#  ARCHIVOS ESTÁTICOS Y MULTIMEDIA
# =====================================================
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'eventos' / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# =====================================================
#  AUTENTICACIÓN
# =====================================================
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/login/'

# =====================================================
#CAMPO POR DEFECTO PARA CLAVES PRIMARIAS
# =====================================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# =====================================================