"""The example plugin: the table's numbers, the page, the panel and the sidebar entry.

The fixture is a real breseq-folder import: two samples of one population, a SNP both carry
and an AMP only the first does. So the first sample has two mutations of which one is shared,
and the second has one, shared.

This plugin is installed in no assembled project, so run these from mutint-core with a
settings module that adds the app -- see CLAUDE.md.
"""

import shutil
import tempfile

from django.contrib.auth.models import User
from django.test import TestCase, override_settings

from mutint_example.util import sample_sharing
from mutint_experiment.models import Experiment
from mutint_import import breseq_folder
from mutint_import.tests import breseq_fixture
from mutint_sample.models import Sample

GD_FIXED = """#=GENOME_DIFF\t1.0
#=REFSEQ\ttest_ref
SNP\t1\t.\ttest_ref\t100\tA\tgene_name=thrA\tgene_product=aspartokinase\tfrequency=1
AMP\t2\t.\ttest_ref\t120\t10\t3\tgene_name=thrA\tgene_product=aspartokinase\tfrequency=1
"""

GD_SHARED = """#=GENOME_DIFF\t1.0
#=REFSEQ\ttest_ref
SNP\t1\t.\ttest_ref\t100\tA\tgene_name=thrA\tgene_product=aspartokinase\tfrequency=1
"""


class _Fixture(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="tester", email="t@e.com",
                                        is_active=True, is_staff=True)
        self.client.force_login(self.user)
        self.drop = tempfile.mkdtemp()
        self.store = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.drop, True)
        self.addCleanup(shutil.rmtree, self.store, True)
        patcher = override_settings(MUTINT_STORE_DIR=self.store)
        patcher.enable()
        self.addCleanup(patcher.disable)
        breseq_fixture.write_sample(self.drop, "1-1-1-1", gd_text=GD_FIXED)
        breseq_fixture.write_sample(self.drop, "1-2-1-1", gd_text=GD_SHARED)
        breseq_folder.import_breseq_folders(
            self.drop, project_name="P", experiment_name="e", owner_name="tester")
        self.experiment = Experiment.objects.get()
        self.first, self.second = Sample.objects.order_by("time_point")


class TableTestCase(_Fixture):
    def test_the_counts(self):
        rows = {row["label"]: row for row in sample_sharing(self.experiment)}
        first, second = rows[self.first.label], rows[self.second.label]
        self.assertEqual((2, 1, 1), (first["mutations"], first["shared"], first["unique"]))
        self.assertEqual((1, 1, 0), (second["mutations"], second["shared"], second["unique"]))

    def test_the_ancestors_mutations_are_left_out(self):
        """Designate the second sample: its SNP is ancestral, so the first sample is left
        with the AMP alone, unique -- and the ancestor itself is no longer a row."""
        self.experiment.set_ancestor(self.second)
        rows = {row["label"]: row for row in sample_sharing(self.experiment)}
        self.assertEqual([self.first.label], list(rows))
        self.assertEqual((1, 0, 1), tuple(rows[self.first.label][k]
                                         for k in ("mutations", "shared", "unique")))

    def test_each_row_links_to_the_samples_page(self):
        row = sample_sharing(self.experiment)[0]
        self.assertEqual("/mutations/breseq?experiment_id=%d&sample_id=%d"
                         % (self.experiment.id, row["sample_id"]), row["url"])


class PageTestCase(_Fixture):
    def test_the_page_renders_the_table_under_the_experiments_header(self):
        response = self.client.get("/example/", {"experiment_id": self.experiment.id})
        self.assertEqual(200, response.status_code)
        html = response.content.decode()
        self.assertIn("P</a>: e</b> - Example", html)
        self.assertIn("mutint-example-table", html)
        self.assertIn(self.first.label, html)

    def test_the_sidebar_and_the_header_bar_carry_the_entry(self):
        html = self.client.get("/example/", {"experiment_id": self.experiment.id}).content.decode()
        self.assertIn('href="/example/?experiment_id=%d">&nbsp;&nbsp;&nbsp;Example</a>'
                      % self.experiment.id, html)

    def test_without_an_experiment_the_page_says_so(self):
        response = self.client.get("/example/")
        self.assertEqual(200, response.status_code)
        self.assertNotIn("mutint-example-table", response.content.decode())


class PanelTestCase(_Fixture):
    def test_the_panel_is_registered_against_this_app(self):
        from mutint_common.panel_registry import get_overview_panels
        panels = [p for p in get_overview_panels() if p["app"] == "mutint_example"]
        self.assertEqual(["Example"], [p["title"] for p in panels])

    def test_the_overview_shows_the_table(self):
        html = self.client.get("/stats", {"experiment_id": self.experiment.id},
                               follow=True).content.decode()
        self.assertIn("mutint-example-table", html)
        self.assertIn("Example page", html)
