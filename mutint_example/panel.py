"""What the Overview panel is handed: the same table the page shows."""

from mutint_example.util import sample_sharing


def example_panel_context(experiment, request):
    return {"rows": sample_sharing(experiment), "experiment_id": experiment.id}
