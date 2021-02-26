from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TransactionTestCase, tag

from modulesApplication.models import Programme


@tag('integration')
class TestProgrammes(TransactionTestCase):
    """Test cases for the Programmes data model."""

    def test_no_duplicate_pks(self):
        """Tests that the primary key constraint behaves as expected."""
        Programme.objects.create(prog_code="1067", title="BSc Computer Science", level="BSC")
        self.assertRaises(IntegrityError, Programme.objects.create, prog_code="1067", title="Fake", level="BSC")

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

    def test_valid_degree_levels_at_database(self):
        """Test that valid degree levels are saved successfully, and that invalid ones are not.
        Checked at the database level."""
        with self.assertRaises(IntegrityError):
            Programme.objects.create(prog_code="1234", title="CompSci", level="foo")
            self.fail("IntegrityError not raised for invalid degree title.")
        self.assertEqual(0, Programme.objects.count())
        Programme.objects.create(prog_code="1234", title="CompSci", level="bsc")
        Programme.objects.create(prog_code="5678", title="MastersDegree", level="msci")
        self.assertEqual(2, Programme.objects.count())

    def test_valid_degree_levels_at_model(self):
        """Tests that programmes saved at the model/form level have valid degree levels. Objects saved
        via a ModelForm are subjected to clean(), so this method tests that."""
        p1 = Programme(prog_code="1234", title="CompSci", level="foo")
        with self.assertRaises(ValidationError):
            p1.clean()
            self.fail("ValidationError not called on invalid degree level.")
