# The example plugin

`mutint-example` is a working plugin small enough to copy: a page in the sidebar's
experiment section, a panel on the experiment's Overview, and an About section, each
registered from one `AppConfig.ready()`. Both the page and the panel show the same table,
of each sample's mutations and how many of them another sample in the experiment carries.

It is installed in no assembled project. To start a plugin of your own, copy the repository,
rename the package, and replace the table with the thing you mean to show; the registrations
stay the same shape.

| Registration | Where | What it gives you |
|---|---|---|
| `register_plugin_urlpatterns` | `apps.py` | your routes under a prefix of your own |
| `register_nav_item` | `apps.py` | a sidebar entry, by `url_name` so a half-install leaves no dead link |
| `register_overview_panel` | `apps.py` | a section on the Overview, body only |
| `register_about_section` | `apps.py` | your paragraph on `/about` |

See the plugin's `CLAUDE.md` for what in the code is worth copying and why.
