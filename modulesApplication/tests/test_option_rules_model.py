from io import StringIO

from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.db import IntegrityError
from django.test import TransactionTestCase
from . import utils

from modulesApplication.database.csv_reader import CsvReader
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

    def test_foreign_key(self):
        """ Test that error thrown is can't find prog_code in Programmes table """
        p = Programme(prog_code="2844", title="BSc Computer Science (Software Engineering) with a YINI", level="BSC")

        self.assertRaises(IntegrityError, OptionRule.objects.create, prog_code=p, entry_year="2018", stage=2,
                          constraint_type="CORE", mod_code_pattern="NEW000")

    def test_simple_squash_core_modules(self):
        # Create three option rules and put them into the database
        base_rule = OptionRule(prog_code=self.p1, entry_year="2019", stage=1,
                               constraint_type="CORE", mod_code_pattern="CS1234")
        other_rule1 = OptionRule(prog_code=self.p1, entry_year="2019", stage=1,
                                 constraint_type="CORE", mod_code_pattern="F00b4r")
        other_rule2 = OptionRule(prog_code=self.p1, entry_year="2019", stage=1,
                                 constraint_type="CORE", mod_code_pattern="wh1zzb4ng")

        OptionRule.objects.bulk_create([base_rule, other_rule1, other_rule2])
        self.assertEqual(3, OptionRule.objects.count(), "To begin with, there are 3 OptionRules.")
        total_minmax = OptionRule.objects.count()
        OptionRule.squash_core_modules(programme=self.p1, entry_year="2019", stage=1)
        self.assertEqual(1, OptionRule.objects.count(), "Redundant OptionRules should be removed from the database.")
        expected_base_rule = OptionRule.objects.first()
        self.assertEqual("CS1234,F00b4r,wh1zzb4ng", expected_base_rule.mod_code_pattern,
                         "The mod_codes of the core modules should be squashed into the first rule's mod_codes")
        self.assertEqual(total_minmax, expected_base_rule.min_quantity,
                         "The minimum quantity of core modules a student must take is ALL of the core modules.")
        self.assertEqual(total_minmax, expected_base_rule.max_quantity,
                         "The maximum quantity is ALSO all of the core modules.")

    def test_complex_squash_core_modules(self):
        utils.read_test_programmes()
        utils.read_test_optionrules()
        bsc = Programme.objects.get(prog_code='1067')
        original_rules = OptionRule.objects.filter(prog_code=bsc, entry_year='2019', stage='1', constraint_type='CORE')
        self.assertEqual(5, original_rules.count(), "There are five core option rules for 1067 in 2019 to begin with.")
        OptionRule.squash_core_modules(programme=bsc, entry_year='2019', stage='1')
        new_rules = OptionRule.objects.filter(prog_code=bsc, entry_year='2019', stage='1', constraint_type='CORE')
        self.assertEqual(1, new_rules.count(), "The five rules have been squashed into one.")
        self.assertEqual("CS1811,CS1840,CS1860,CS1870,CS1890", new_rules[0].mod_code_pattern,
                         "The mod_code_patterns have been squashed into the remaining rule.")

    def test_squash_optional_modules(self):
        """Tests that we can read optional modules from 'optional_modules_by_programme', and squash them into
        the relevant OptionRules entries."""
        utils.read_test_programmes()
        utils.read_test_optionrules()
        bsc = Programme.objects.get(prog_code='1067')
        cr = CsvReader()
        optional_modules = cr.read_dict(
            'modulesApplication/tests/resources/optional_modules_by_programme.csv')

        # Stage 2 of BSc Computer Science, 2019
        expected_pattern = "CS2900,CS2910,IY2840"
        OptionRule.squash_opts_modules(optional_modules, programme=bsc, entry_year='2019', stage='2')
        actual_pattern = OptionRule.objects.get(
            prog_code=bsc, entry_year='2019', stage='2', constraint_type='OPTS').mod_code_pattern
        self.assertEqual(expected_pattern, actual_pattern)

        # Stage 3 of BSc Computer Science, 2019
        expected_pattern = "CS3000,CS3003,CS3110,CS3220,CS3250,CS3470,CS3480,CS3490,CS3510,CS3580,CS3750,CS3840,CS3846,CS3870,CS3920,CS3930,CS3940,CS3945,IY3501,IY3606,IY3609,IY3612,IY3660,IY3840"
        OptionRule.squash_opts_modules(optional_modules, programme=bsc, entry_year='2019', stage='3')
        actual_pattern = OptionRule.objects.get(
            prog_code=bsc, entry_year='2019', stage='3', constraint_type='OPTS').mod_code_pattern
        self.assertMultiLineEqual(expected_pattern, actual_pattern)
