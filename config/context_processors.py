"""
Context processors required by aledb-core's template settings.
This module must exist here because aledb-core's TEMPLATES config references
`config.context_processors.global_settings`, and `config` resolves to this
package at runtime.
"""
from django.conf import settings


def global_settings(request):
    return {
        'GOOGLE_ANALYTICS_TAG': settings.GOOGLE_ANALYTICS_TAG,
    }
