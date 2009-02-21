# Django deployment settings for jksite project.
from settings import *

DEBUG = False
TEMPLATE_DEBUG = False

DATABASE_ENGINE = 'mysql'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'jeknowledge_jksite'             # Or path to database file if using sqlite3.
DATABASE_USER = 'jeknowledge'             # Not used with sqlite3.
DATABASE_PASSWORD = '8Huhzj/u'         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Override the server-derived value of SCRIPT_NAME 
# See http://code.djangoproject.com/wiki/BackwardsIncompatibleChanges#lighttpdfastcgiandothers
FORCE_SCRIPT_NAME = ''