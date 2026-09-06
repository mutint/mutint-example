from django.urls import re_path

from mutint_example import views

# Mounted at ^example/ (apps.py). One route; the sidebar's entry reverses its name.
urlpatterns = [
    re_path(r'^$', views.example, name='example'),
]
