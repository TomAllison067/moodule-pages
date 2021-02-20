from django.test import TestCase

from modulesApplication.models import OptionRule, Programme
from modulesApplication.tests import utils


class TestOptionRulesSquash(TestCase):

    def test_simple_squash_core_modules(self):
        # Create three option rules and put them into the database
        p1 = Programme.objects.create(prog_code="BSc FooScience", level="BSc")
        base_rule = OptionRule(prog_code=p1, entry_year="2019", stage=1,
                               constraint_type="CORE", mod_code_pattern="CS1234")
        other_rule1 = OptionRule(prog_code=p1, entry_year="2019", stage=1,
                                 constraint_type="CORE", mod_code_pattern="F00b4r")
        other_rule2 = OptionRule(prog_code=p1, entry_year="2019", stage=1,
                                 constraint_type="CORE", mod_code_pattern="wh1zzb4ng")
        OptionRule.objects.bulk_create([base_rule, other_rule1, other_rule2])

        # Sanity check
        self.assertEqual(3, OptionRule.objects.count(), "To begin with, there are 3 OptionRules.")
        total_minmax = OptionRule.objects.count()

        # Squash!
        OptionRule.squash_core_modules(programme=p1, entry_year="2019", stage=1)
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
