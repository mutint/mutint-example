"""
Local development overrides — not committed to version control.
Copy this file or import it and override values as needed.
"""
from .settings import *  # noqa: F401, F403

DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'mutint_app_local.sqlite3'),
    }
}
