# CLAUDE.md — mutint-example

The example plugin: one of everything a plugin is likely to want, kept small enough to read
in one sitting and copy. A page in the sidebar's experiment section (**Example**, at
`/example/`), a panel on the experiment's Overview (also **Example**), and an About section,
each registered from `mutint_example/apps.py`. Both the page and the panel render the same
table, from `util.sample_sharing`: each sample's mutations, how many of those another sample
carries too, and how many are its own.

**It is a stub, installed nowhere.** It is not in `mutint/.gitmodules` or `aledb/.gitmodules`
and should not be; a real feature belongs in a plugin of its own, started by copying this
one. It was `mutint-app`, the assembled project's "own app", which registered nothing and
existed to carry MutInt's name and version for the sidebar. MutInt names itself in its own
`config/version.py` now.

**What is worth copying** is the shape rather than the table: `calls_for_samples` rather
than a bare `MutationCall.objects.filter`, so the designated ancestor is subtracted at the
derivation and not at the render; `values_list` tuples rather than model instances; a
`url_name` on the nav entry so a half-installed plugin cannot leave a dead link; a panel
template that is the body only; and a page that gets its experiment through
`mutint_sample.views.common.get_experiment`, which checks permission and answers the
no-experiment page for you.

## Tests

The plugin is installed in no assembled project, so its tests run from mutint-core with a
settings module that adds the app:

```bash
cd mutint-core
cat > /tmp/example_settings.py <<'PY'
from config.settings_local import *  # noqa: F401,F403
INSTALLED_APPS = INSTALLED_APPS + ["mutint_example"]
PY
DJANGO_SETTINGS_MODULE=example_settings PYTHONPATH=/tmp:../mutint-example ./mutint test mutint_example
```
