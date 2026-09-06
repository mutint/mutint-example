"""The Example page: the sample-sharing table, under the experiment's header."""

import logging

from django.http import HttpResponse
from django.template import loader

import mutint_sample.views.common
from mutint_common.logger import user_extra
from mutint_common.util import get_user_context
from mutint_experiment import models
from mutint_example.util import sample_sharing

logger = logging.getLogger(__name__)


def example(request):
    context = get_user_context(request.user)
    try:
        # The experiment from `?experiment_id=`, permission checked; without one, the page
        # every experiment view shows in that case.
        experiment = mutint_sample.views.common.get_experiment(request)
    except models.Experiment.DoesNotExist:
        return mutint_sample.views.common.no_experiment_selected(
            request, context, logger, "example")
    context.update({
        "experiment_id": experiment.id,
        "experiment_name": experiment.name,
        "project_name": experiment.project.name,
        "project_id": experiment.project.id,
        "title": experiment.name + " Example",
        "rows": sample_sharing(experiment),
    })
    logger.info("example page", extra=user_extra(request))
    return HttpResponse(loader.get_template("example/page.html").render(context, request))
