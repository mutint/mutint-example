"""
Thin shim so `config.views` resolves to this package (not aledb-core's).
Re-exports everything from aledb-core's config/views.py via importlib to
avoid the `config` namespace collision.
"""
import importlib.util
import os

_core_views = importlib.util.spec_from_file_location(
    '_aledb_core_views',
    os.path.join(os.path.dirname(os.path.dirname(__file__)), 'aledb-core', 'config', 'views.py'),
)
_mod = importlib.util.module_from_spec(_core_views)
_core_views.loader.exec_module(_mod)

protected_file_serve = _mod.protected_file_serve
