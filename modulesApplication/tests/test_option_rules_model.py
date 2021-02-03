from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TransactionTestCase

from modulesApplication.models import OptionRule, Programme


class TestOptionRule(TransactionTestCase):
    """
    Tests to create Option_rules table
    """

    def setUp(self):
        self.p1 = Programme(prog_code="1067", title="BSc Computer Science", level="BSC")
        self.p1.save()
        Programme.objects.create(prog_code="1059", title="BSc Computer Science (Artificial Intelligence)", level="BSC")
        Programme.objects.create(prog_code="2675", title="BSc Computer Science (Information Security)", level="BSC")
        Programme.objects.create(prog_code="2843", title="BSc Computer Science (Software Engineering)", level="BSC")

    def test_save_rule(self):
        """  """
        OptionRule.objects.create(prog_code=self.p1, entry_year="2019", stage=2,
                                  constraint_type="CORE", mod_code_pattern="CS2810")
        self.assertEqual(OptionRule.objects.count(), 1, "Sucessfully creating an rule")

    def test_default_quantity(self):
        OptionRule.objects.create(prog_code=self.p1, entry_year="2018", stage=2,
                                  constraint_type="OPTS", mod_code_pattern="IT2345")
        self.assertIsNotNone(OptionRule.objects.get(prog_code="1067").min_quantity,
                             "Unassigned min_quantity, should recives default value")

        self.assertEqual(OptionRule.objects.get(prog_code="1067").min_quantity, 1,
                         "When min_quantity is unassigned, default value is 1")
        self.assertEqual(OptionRule.objects.get(prog_code="1067").max_quantity, 1,
                         "Didn't assign a max_quantity value, hence should get default of 1")

    def test_null_fields_error(self):
        """ Test throwing error is all relevant fields are unassigned """

        self.assertRaises(ValidationError, OptionRule.objects.create, prog_code=self.p1)
        self.assertRaises(IntegrityError, OptionRule.objects.create, prog_code=self.p1, constraint_type="CORE")

    def test_constraint_type(self):
        """ test that constraint has to be one of the choices """
        with self.assertRaises(ValidationError):
            OptionRule.objects.create(prog_code=self.p1, entry_year="2018", stage=2,
                                      constraint_type="anotherfail", mod_code_pattern="IT2345")
            self.fail("Validation error not raised for invalid degree title.")

    def test_feature_grouping_core(self):
        """ Test trying to group together all core modules"""
        OptionRule.objects.create(prog_code=self.p1, entry_year="2018", stage=2,
                                  constraint_type="CORE", mod_code_pattern="AB2345")
        OptionRule.objects.create(prog_code=self.p1, entry_year="2018", stage=2,
                                  constraint_type="CORE", mod_code_pattern="YZ0987")
        OptionRule.objects.create(prog_code=self.p1, entry_year="2018", stage=2,
                                  constraint_type="CORE", mod_code_pattern="NEW000")
        self.assertEqual(1, OptionRule.objects.count(),
                         "multiple objects should group together core modules if in same year, stage and programme")
        self.assertEqual(OptionRule.objects.get(prog_code="1067").mod_code_pattern, "AB2345, YZ0987, NEW000")

    def test_foreign_key(self):
        """ Test that error thrown is can't find prog_code in Programmes table """
        p = Programme(prog_code="2844", title="BSc Computer Science (Software Engineering) with a YINI", level="BSC")

        self.assertRaises(IntegrityError, OptionRule.objects.create, prog_code=p, entry_year="2018", stage=2,
                          constraint_type="CORE", mod_code_pattern="NEW000")

