from django.apps import AppConfig


class MutintAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mutint_app'
    verbose_name = 'MutInt App'

    def ready(self):
        from aledb_common.about_registry import register_about_section

        register_about_section(self, name='mutint-app',
                               template='about/sections/mutint_app.html')
