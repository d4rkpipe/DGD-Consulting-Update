"""
Django settings for dgd_backend project.
"""

from pathlib import Path
from decouple import config, Csv
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# ─── Security ──────────────────────────────────────────────
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=Csv())

# ─── Applications ──────────────────────────────────────────
INSTALLED_APPS = [
    # jazzmin must come BEFORE admin
    'jazzmin',

    # modeltranslation must come BEFORE admin
    'modeltranslation',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd party
    'rest_framework',
    'corsheaders',
    'ckeditor',
    'ckeditor_uploader',

    # local apps
    'services',
    'blog',
    'contacts',
    'partners',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',          # CORS — first
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',     # for i18n
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'dgd_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'dgd_backend.wsgi.application'

# ─── Database ──────────────────────────────────────────────
_db_url = config('DATABASE_URL', default='').strip()
if _db_url:
    DATABASES = {'default': dj_database_url.parse(_db_url, conn_max_age=600)}
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ─── Password validation ───────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ─── Internationalization ──────────────────────────────────
LANGUAGE_CODE = 'uz'
TIME_ZONE = 'Asia/Tashkent'
USE_I18N = True
USE_TZ = True

LANGUAGES = [
    ('uz', "O'zbek"),
    ('ru', 'Русский'),
    ('en', 'English'),
    ('tr', 'Türkçe'),
]

# modeltranslation
MODELTRANSLATION_DEFAULT_LANGUAGE = 'uz'
MODELTRANSLATION_LANGUAGES = ('uz', 'ru', 'en', 'tr')
MODELTRANSLATION_FALLBACK_LANGUAGES = ('uz', 'en', 'ru', 'tr')

LOCALE_PATHS = [BASE_DIR / 'locale']

# ─── Static & Media ────────────────────────────────────────
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ─── REST Framework ────────────────────────────────────────
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 12,
}

# ─── CORS ──────────────────────────────────────────────────
CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS',
    default='http://localhost:8000,http://127.0.0.1:8000',
    cast=Csv()
)
CORS_ALLOW_CREDENTIALS = True

# ─── Email (Gmail SMTP) ────────────────────────────────────
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@example.com')
ADMIN_EMAIL = config('ADMIN_EMAIL', default='admin@example.com')

# Use console backend if no password set (so dev doesn't crash without Gmail creds)
if not EMAIL_HOST_PASSWORD or EMAIL_HOST_PASSWORD == 'your-app-password-here':
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# ─── Telegram bot (kontakt formasi xabari) ──────────────────
TELEGRAM_BOT_TOKEN = config('TELEGRAM_BOT_TOKEN', default='')
# vergul bilan ajratilgan admin Telegram ID'lari (raqamlar)
_tg_ids = config('TELEGRAM_ADMIN_IDS', default='')
TELEGRAM_ADMIN_IDS = [
    int(x.strip()) for x in _tg_ids.split(',') if x.strip().isdigit()
]

# ─── Jazzmin (admin theme) ─────────────────────────────────
JAZZMIN_SETTINGS = {
    'site_title':  'DGD Consulting Admin',
    'site_header': 'DGD Consulting',
    'site_brand':  'DGD Consulting',
    'site_logo':   None,
    'login_logo':  None,
    'site_icon':   None,
    'welcome_sign': 'DGD Consulting boshqaruv paneliga xush kelibsiz',
    'copyright':   'DGD Consulting MChJ',

    # Search across these models from the top bar
    'search_model': ['blog.BlogPost', 'services.Service'],

    # Top menu links
    'topmenu_links': [
        {'name': 'Bosh sayt', 'url': 'http://localhost:8000/', 'new_window': True},
        {'name': 'API',       'url': '/api/services/',         'new_window': True},
        {'model': 'auth.User'},
    ],

    # User menu (top right)
    'usermenu_links': [
        {'name': "DGD Consulting saytiga o'tish", 'url': 'http://localhost:8000/', 'new_window': True, 'icon': 'fas fa-globe'},
    ],

    # Sidebar
    'show_sidebar': True,
    'navigation_expanded': True,
    'order_with_respect_to': [
        'blog', 'services', 'partners', 'contacts', 'auth',
    ],

    # Icons per model (FontAwesome 5)
    'icons': {
        'auth':                       'fas fa-users-cog',
        'auth.user':                  'fas fa-user',
        'auth.Group':                 'fas fa-users',
        'blog.BlogPost':              'fas fa-newspaper',
        'blog.Category':              'fas fa-tags',
        'services.Service':           'fas fa-cogs',
        'partners.Partner':           'fas fa-handshake',
        'contacts.ContactSubmission': 'fas fa-envelope-open-text',
        'contacts.NewsletterSubscriber': 'fas fa-paper-plane',
    },
    'default_icon_parents':   'fas fa-chevron-circle-right',
    'default_icon_children':  'fas fa-circle',

    # UI Customisations
    'related_modal_active': True,
    'custom_css':  None,
    'custom_js':   None,
    'use_google_fonts_cdn': True,
    'show_ui_builder': False,

    # Change form template — collapsible/tabs
    'changeform_format': 'collapsible',
    'changeform_format_overrides': {
        'blog.BlogPost':       'horizontal_tabs',
        'services.Service':    'horizontal_tabs',
        'blog.Category':       'horizontal_tabs',
    },

    # Language switcher (admin UI language)
    'language_chooser': True,
}

JAZZMIN_UI_TWEAKS = {
    'navbar_small_text':   False,
    'footer_small_text':   False,
    'body_small_text':     False,
    'brand_small_text':    False,
    'brand_colour':        'navbar-success',
    'accent':              'accent-success',
    'navbar':              'navbar-dark navbar-success',
    'no_navbar_border':    False,
    'navbar_fixed':        True,
    'layout_boxed':        False,
    'footer_fixed':        False,
    'sidebar_fixed':       True,
    'sidebar':             'sidebar-dark-success',
    'sidebar_nav_small_text':       False,
    'sidebar_disable_expand':       False,
    'sidebar_nav_child_indent':     True,
    'sidebar_nav_compact_style':    False,
    'sidebar_nav_legacy_style':     False,
    'sidebar_nav_flat_style':       False,
    'theme':               'default',
    'dark_mode_theme':     'darkly',
    'button_classes': {
        'primary': 'btn-success',
        'secondary': 'btn-outline-secondary',
        'info':      'btn-info',
        'warning':   'btn-warning',
        'danger':    'btn-danger',
        'success':   'btn-success',
    },
}

# ─── CKEditor ──────────────────────────────────────────────
CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_IMAGE_BACKEND = 'pillow'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Basic',
        'height': 400,
        'width': '100%',
        'toolbar_Basic': [
            ['Bold', 'Italic', 'Underline', '-', 'NumberedList', 'BulletedList',
             '-', 'Link', 'Unlink', '-', 'Image', '-', 'Source'],
            ['Format', '-', 'RemoveFormat'],
        ],
    },
}
