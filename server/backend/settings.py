import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = os.getenv('SECRET_KEY', '*6k@6^#8iww1r_iy1wc-!76h%zqbc6=h_&e9y=^3(leg7-1hff')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.getenv('DEBUG', False))

ALLOWED_HOSTS = ['localhost', '*']


def show_toolbar(request):
    return True


DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': 'backend.settings.show_toolbar',
}

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'rest_framework',
    'drf_yasg',
    'corsheaders',
    'admin_reorder',
    'app',
    'users_system',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'admin_reorder.middleware.ModelAdminReorder',
]

if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'backend/templates'),
        ],
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

WSGI_APPLICATION = 'backend.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'postgres'),
        'USER': os.getenv('POSTGRES_USER', 'postgres'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'postgres'),
        'HOST': os.getenv('POSTGRES_HOST', 'postgres'),
        'PORT': os.getenv('POSTGRES_PORT', '5432'),
    }
}

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


ADMIN_SITE_HEADER = "Администрирование"

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATIC_ROOT = 'static'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_METADATA_CLASS': 'rest_framework.metadata.SimpleMetadata',
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 50
}

DEFAULT_AUTO_FIELD='django.db.models.AutoField'

LOGGING = {
    'version': 1,
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console'],
        }
    }
}

ADMIN_REORDER = (
    {'app': 'app', 'label': 'Объекты', 'models': (
        'app.Asset',
        'app.AssetType',
        'app.Interface',
        'app.Vendor'
    )},
    {'app': 'app', 'label': 'Угрозы', 'models': (
        'app.Threat',
        'app.ThreatsImplementationMethod',
        'app.ThreatsImplementationMethodGroup',
    )},
    {'app': 'app', 'label': 'Уязвимости', 'models': (
        'app.Vulnerability',
    )},
    {'app': 'app', 'label': 'Нарушители', 'models': (
        'app.Attacker',
        'app.AttackerSpecification',
        'app.Capability',
        'app.Scope',
        'app.AttackerScope',
    )},
    {'app': 'app', 'label': 'Негативные последствия', 'models': (
        'app.NegativeConsequence',
        'app.NegativeConsequenceGroup',
    )},
    {'app': 'app', 'label': 'Сценарий', 'models': (
        'app.Scenario',
        'app.ScenarioStep',
        'app.Tactic',
        'app.Technique',
    )},
    {'app': 'app', 'label': 'Системы', 'models': (
        'app.ISPDNClass',
        'app.GISClass',
        'app.ASUTPClass',
        'app.KIIClass',
    )},
    {'app': 'users_system', 'label': 'Пользовательские системы', 'models': (
        'users_system.System',
    )},
)

CORS_ALLOW_ALL_ORIGINS = True