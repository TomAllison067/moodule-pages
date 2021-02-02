from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TransactionTestCase

from modulesApplication.models import Programme


class TestProgrammes(TransactionTestCase):
    """Test cases for the Programmes data model."""
    def test_one_programme_saved(self):
        """Tests programme saving."""
        Programme.objects.create(prog_code="1067", title="BSc Computer Science", level="BSC")
        self.assertEqual(1, Programme.objects.count(), "One programme saves successfully.")

    def test_no_duplicate_pks(self):
        """Tests that the primary key constraint behaves as expected."""
        Programme.objects.create(prog_code="1067", title="BSc Computer Science", level="BSC")
        self.assertRaises(IntegrityError, Programme.objects.create, prog_code="1067", title="Fake", level="BSC")

    def test_two_programmes(self):
        """Tests programme saving."""
        Programme.objects.create(prog_code="1067", title="BSc Computer Science", level="BSC")
        Programme.objects.create(prog_code="1059", title="BSc Computer Science (Artificial Intelligence)", level="BSC")
        self.assertEqual(2, Programme.objects.count(), "Two programmes save successfully.")

    def test_yini(self):
        """
        Tests that saving fields with different YINI values behaves as expected.
        """
        Programme.objects.create(prog_code="1067", title="No YINI", level="BSC", yini=0)
        Programme.objects.create(prog_code="1068", title="YINI", level="BSC", yini=1)
        self.assertEqual(2, Programme.objects.count(), "Two programmes total.")
        self.assertEqual(1, Programme.objects.filter(yini=1).count(), "Only one programme with YINI.")
        with self.assertRaises(ValidationError):  # Test the validation of the BooleanField, a boolean can be 0 or 1
            Programme.objects.create(prog_code="1079", title="YINI3", level="BSC", yini=3)

    def test_unique_title(self):
        """Tests that an IntegrityError is raised when the unique constraint on title is violated.
        This is enforced at the database level AND validation level."""
        Programme.objects.create(prog_code="1234", title="CompSci", level="BSC")
        with self.assertRaises(IntegrityError):
            Programme.objects.create(prog_code="5678", title="CompSci", level="BSC")
            self.fail("IntegrityError not raised for duplicate programme title.")
