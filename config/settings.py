"""
Base settings for mutint-app standalone development.

Strategy: load aledb-core's defaults by file path using importlib so we inherit
all core settings without importing aledb-core's `config` package (which would
shadow this project's own `config` package on sys.path).
"""
import importlib.util
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ── Path setup ────────────────────────────────────────────────────────────────
# Make aledb-core's app packages importable (e.g. `import aledb_experiment`).
# Append rather than insert so that `import config` still resolves to THIS
# project's config/ directory (BASE_DIR was inserted first by manage.py).
_ALEDB_CORE_DIR = os.path.join(BASE_DIR, 'aledb-core')
if _ALEDB_CORE_DIR not in sys.path:
    sys.path.append(_ALEDB_CORE_DIR)

# ── Inherit aledb-core base settings ─────────────────────────────────────────
# Load config/defaults.py from aledb-core by path to avoid the namespace clash.
def _load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

_core_defaults = _load_module(
    '_aledb_core_defaults',
    os.path.join(_ALEDB_CORE_DIR, 'config', 'defaults.py'),
)
# Pull every uppercase name (Django settings convention) into this module.
globals().update({k: getattr(_core_defaults, k) for k in dir(_core_defaults) if k.isupper()})

# ── Override settings that depend on project root ────────────────────────────
# BASE_DIR from aledb-core's defaults points to aledb-core/.  Reset it here.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

ROOT_URLCONF = 'config.urls'          # resolves to mutint-app/config/urls.py
WSGI_APPLICATION = 'config.wsgi.application'

# ── Add mutint-specific apps ──────────────────────────────────────────────────
INSTALLED_APPS = INSTALLED_APPS + [
    'mutint_app',
]
