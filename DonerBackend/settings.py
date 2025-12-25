from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-f3h)&5s&%up@r(h^fgz*+-^qg5e9ui)&f1x9&i2nvz&c_^xu-q'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Api.apps.ApiConfig',
    'djoser',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
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
]

ROOT_URLCONF = 'DonerBackend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'DonerBackend.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

JAZZMIN_SETTINGS = {
    "site_title": "Doner Admin",
    "site_header": "Doner Admin Panel",
    "site_brand": "Doner",
    "welcome_sign": "Doner Admin Paneliga hoş geldiňiz!",
    "copyright": "Doner",

    # LOGO
    "site_logo": "logo.png",  # static/logo.png bo‘lsin
    "login_logo": "logo.png",

    # SEARCH MODEL FIELD
    "search_model": "auth.User",

    # TOP MENU
    "topmenu_links": [
        {"name": "Hasabat", "url": "admin:dashboard", "permissions": ["auth.view_user"]},
        {"model": "app.Users"},
        {"model": "app.Product"},
        {"model": "app.Order"},
        {"app": "app"},
    ],

    # SIDEBAR MENUS
    "navigation_expanded": True,
    "order_with_respect_to": [
        "app",
        "auth",
    ],

    "icons": {
        "app.Users": "fas fa-user",
        "app.Product": "fas fa-box",
        "app.ProductImage": "fas fa-image",
        "app.WarehouseName": "fas fa-warehouse",
        "app.Warehouse": "fas fa-cubes",
        "app.ProductWarehouse": "fas fa-layer-group",
        "app.Cart": "fas fa-shopping-cart",
        "app.Order": "fas fa-receipt",
        "app.OrderItem": "fas fa-list",
        "app.Payment": "fas fa-money-bill",
        "app.HomePicture": "fas fa-images",
    },

    # UI CUSTOM
    "show_ui_builder": True,
}
JAZZMIN_UI_TWEAKS = {
    "theme": "flatly",  # Yoqimli yashil rang
    "dark_mode_theme": "darkly",
    "navbar": "navbar-dark",
    "navbar_fixed": True,
    "footer_fixed": True,
    "sidebar": "sidebar-light",
    "sidebar_fixed": True,
    "actions_sticky_top": True,
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        'rest_framework.authentication.TokenAuthentication',
    )
}

DJOSER = {
    'SERIALIZERS': {
       'current_user': 'Api.serializers.CustomUserSerializer',
    }
}

LANGUAGE_CODE = 'tk'

TIME_ZONE = 'Asia/Ashgabat'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'statics/'
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'
STATIC_ROOT = BASE_DIR / 'Api/static'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'Api.Users'
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_OPTIONS = [
    'http://localhost:8000',
    'http://192.168.100.211:8000',
    'http://10.238.77.192:8000',
]
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'PUT',
    'DELETE',
]
APPEND_SLASH=False