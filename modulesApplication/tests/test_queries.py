from io import StringIO

from django.core.management import call_command
from django.test import TransactionTestCase

from modulesApplication.database import queries as db
from modulesApplication.database.models.programme import Programme
from modulesApplication.models import Module, Strands
from modulesApplication.tests import utils


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

    def test_query_modcode_patterns(self):
        """Tests that we can get a dictionary of module code patterns for a given degree, entry year and stage 1."""
        utils.read_test_programmes()
        utils.read_test_optionrules()
        degree = Programme.objects.get(prog_code='1067')

        # TEST 1 - BSc Computer Science, entry year 2019, stage 1
        # The expected core and discretionary modules for Computer Science, stage 1, entry year 2019
        expected = {'CORE': ['CS1811', 'CS1840', 'CS1860', 'CS1870', 'CS1890'],
                    'DISC_ALT': ['CS1812', 'CS1813', 'CS1822', 'CS1821']}

        mod_codes = db.modcode_patterns_by_constraint(degree, '2019', '1')
        self.assertEqual(expected, mod_codes)

        # TEST 2 - BSc Computer Science, entry year 2019, stage 2
        expected = {'CORE': ['CS2800', 'CS2810', 'CS2850', 'CS2855', 'CS2860', 'IY2760'],
                    'OPTS': ['CS2', 'IY2']}
        mod_codes = db.modcode_patterns_by_constraint(degree, '2019', '2')
        self.assertEqual(expected, mod_codes)

        # TEST 3 - BSc Computer Science, entry year 2019, stage 3
        expected = {'CORE': ['CS3821'], 'OPTS': ['CS3', 'IY3']}
        mod_codes = db.modcode_patterns_by_constraint(degree, '2019', '3')
        self.assertEqual(expected, mod_codes)