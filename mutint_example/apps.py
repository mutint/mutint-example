from django.apps import AppConfig


class ExampleConfig(AppConfig):
    """The example plugin: one of everything a plugin is likely to want, kept small.

    It contributes a page in the experiment section (**Example**, at `/example/`), a panel
    on the experiment's Overview (also **Example**), and an About section -- and both the
    page and the panel show the same table, of each sample's mutation count and how many of
    those it shares with another sample. Nothing here is a feature; the table exists so the
    registrations have something real to render, and a reader copying this repo starts with
    working code rather than a skeleton.

    It was `mutint-app`, the assembled project's "own app", which registered nothing and
    carried MutInt's name and version for the sidebar. MutInt names itself in its own
    `config/` now, and this is a plugin like any other: installed by listing it in
    `.gitmodules`, and installed in MutInt only.
    """

    name = 'mutint_example'

    def ready(self):
        from django.urls import include, re_path
        from mutint_common.about_registry import register_about_section
        from mutint_common.nav_registry import EXPERIMENT_SECTION, register_nav_item
        from mutint_common.panel_registry import register_overview_panel
        from mutint_common.plugin_registry import register_plugin_urlpatterns
        from mutint_example.panel import example_panel_context

        # A page: its routes, mounted under a prefix of its own, and a sidebar entry in the
        # experiment section by `url_name`, so a half-installed plugin leaves no dead link.
        register_plugin_urlpatterns([
            re_path(r'^example/', include('mutint_example.urls')),
        ])
        register_nav_item('Example', url_name='example', section=EXPERIMENT_SECTION)

        # A panel on the Overview: the body only, under a heading the page draws.
        register_overview_panel(self, name='example', title='Example',
                                template='example/panel.html',
                                context=example_panel_context)

        register_about_section(self, name='mutint-example',
                               template='about/sections/mutint_example.html')
