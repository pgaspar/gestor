# Django settings for jksite project.
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# nmariz hacking:
ROOT_PATH = os.path.realpath(os.path.dirname(__file__))


ADMINS = (
    ('Pedro Gaspar', 'pedro.gaxpar@gmail.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'jksite.sqlite3'             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Lisbon'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1
BASE_DOMAIN = "http://jeknowledge.com"

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
#MEDIA_ROOT = ''
MEDIA_ROOT = os.path.join(ROOT_PATH, 'media/')


# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '(n%11p2k8lh(lwhq2(obb_gxj!6n2w0$rn91w1f5$5h77j(7tw'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
	#'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
	#'middleware.requirelogin.RequireLoginMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'accounts.backends.EmailOrUsernameModelBackend',
    'django.contrib.auth.backends.ModelBackend'
)

ROOT_URLCONF = 'jksite.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
	os.path.join(ROOT_PATH, 'templates'),

)

TEMPLATE_CONTEXT_PROCESSORS = (
	"django.core.context_processors.auth",
	"django.core.context_processors.media",
	"django.core.context_processors.request",
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
	'django.contrib.admin',
	'django.contrib.humanize',
	'django.contrib.markup',
    'django_evolution',
	#'extensions',
	'accounts',
	'gestor',
	'cvmanager',
	'mainsite',
    'formacao',
	'sorl.thumbnail',
)

DATE_FORMAT = "d/F/Y"

AUTH_PROFILE_MODULE = "accounts.userprofile"

FIXTURE_DIRS = os.path.join(ROOT_PATH, 'fixtures')

DEFAULT_AVATAR = u'photos/default.png'

THUMBNAIL_SUBDIR = '_thumbs'

# SMTP
EMAIL_HOST = 'mail.wservices.ch'
EMAIL_HOST_USER = 'gestor@jeknowledge.com'
EMAIL_HOST_PASSWORD = 'bxe52ows'
DEFAULT_FROM_EMAIL = 'gestor@jeknowledge.com'
