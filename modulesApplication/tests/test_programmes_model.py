from django.db import IntegrityError
from django.test import TransactionTestCase

from modulesApplication.models import Programme


class TestProgrammes(TransactionTestCase):
    def test_one_programme_saved(self):
        Programme.objects.create(prog_code="1067", title="BSc Computer Science", level="BSC")
        self.assertEqual(1, Programme.objects.count(), "One programme saves successfully.")

    def test_no_duplicate_pks(self):
        Programme.objects.create(prog_code="1067", title="BSc Computer Science", level="BSC")
        self.assertRaises(IntegrityError, Programme.objects.create, prog_code="1067", title="Fake", level="BSC")

    def test_two_programmes(self):
        Programme.objects.create(prog_code="1067", title="BSc Computer Science", level="BSC")
        Programme.objects.create(prog_code="1059", title="BSc Computer Science (Artificial Intelligence)", level="BSC")
        self.assertEqual(2, Programme.objects.count(), "Two programmes save successfully.")