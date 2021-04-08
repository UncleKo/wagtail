from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'o8lwj+$1-bwbw6o)c)fvp^j7ivlowv)_e%73)i^&@%x&o#6+yt'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*'] 

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

INSTALLED_APPS = INSTALLED_APPS + [
  'wagtail.contrib.styleguide',
]


try:
    from .local import *
except ImportError:
    pass
