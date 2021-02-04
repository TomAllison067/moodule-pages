from io import StringIO

from django.core.management import call_command
from django.test import TransactionTestCase

from modulesApplication.database.csv_reader import CsvReader
from modulesApplication.database.models.option_rule import OptionRule
from modulesApplication.database.models.programme import Programme
from modulesApplication.models import Module, Strands


class TestQueries(TransactionTestCase):
    """
    A class to test queries that involve more than one data model, eg joins.
    """

    def test_query_modules_by_strand(self):
        """
        Tests that all the foreign keys of each strand are the same as all the primary keys of the modules in that
        strand.
        This takes a set of all foreign keys for each strand, a set of all primary keys for the modules that
        should be referenced by that strand, and asserts that each set is the same.
        :return:
        """
        # Load the test data
        output = StringIO()  # Silence the import success message for test purposes
        call_command('import_test_data', stdout=output)

        # All the module codes referenced by the infosec strand
        infosec_strands_foreignkeys = set(Strands.objects.filter(strand="IS").values_list('module', flat=True))
        infosec_modules_primarykeys = set(Module.objects.filter(strands__strand="IS")
                                          .values_list('mod_code', flat=True))
        self.assertEqual(infosec_modules_primarykeys,
                         infosec_strands_foreignkeys, "The primary and foreign keys do not match for the IS strand.")

        # SE strand
        se_strands_foreignkeys = set(Strands.objects.filter(strand="SE").values_list('module', flat=True))
        se_modules_pks = set(Module.objects.filter(strands__strand="SE")
                             .values_list('mod_code', flat=True))
        self.assertEqual(se_modules_pks, se_strands_foreignkeys,
                         "The primary and foreign keys do not match for the SE strand.")

        # AI strand
        ai_strands_foreignkeys = set(Strands.objects.filter(strand="AI").values_list('module', flat=True))
        ai_modules_pks = set(Module.objects.filter(strands__strand="AI")
                             .values_list('mod_code', flat=True))
        self.assertEqual(ai_modules_pks, ai_strands_foreignkeys,
                         "The primary and foreign keys do not match for the AI strand.")
        # DNS strand
        dns_strands_foreignkeys = set(Strands.objects.filter(strand="DNS").values_list('module', flat=True))
        dns_modules_pks = set(Module.objects.filter(strands__strand="DNS")
                              .values_list('mod_code', flat=True))
        self.assertEqual(dns_modules_pks, dns_strands_foreignkeys,
                         "The primary and foreign keys do not match for the DNS strand.")

    def test_query_modules(self):
        cr = CsvReader()
        # Read in the programmes
        programmes = cr.read_table_partial(
            filepath="modulesApplication/tests/resources/programmes.csv",
            model_class=Programme
        )
        Programme.objects.bulk_create(programmes)

        # Read in the rules
        rules = cr.read_table_partial(
            filepath="modulesApplication/tests/resources/option_rules.csv",
            model_class=OptionRule
        )
        OptionRule.objects.bulk_create(rules)

        degree = Programme.objects.get(prog_code='1067')  # Get 'BSc Computer Science'

        # Get the OptionRule for the degree, entry year 2019 stage 1
        OptionRule.squash_core_modules(programme=degree, entry_year='2019', stage='1')  # Squash cos it's nice
        degree_options = OptionRule.objects.filter(prog_code=degree, entry_year='2019', stage='1')

        # Put the module codes allowed by the rules into a dict
        mod_codes = {}
        for option in degree_options:
            mod_codes[option.constraint_type] \
                = mod_codes.get(option.constraint_type, []) + [m for m in option.mod_code_pattern.split(',')]

        # What we know the core and discretionary modules for year 1 Computer Science are
        expected = {'CORE': ['CS1811', 'CS1840', 'CS1860', 'CS1870', 'CS1890'],
                    'DISC_ALT': ['CS1812', 'CS1813', 'CS1822', 'CS1821']}
        self.assertEqual(expected, mod_codes)  # Check we're correct
