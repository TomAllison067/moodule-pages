from django.core.management import call_command
from django.test import TransactionTestCase

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
        call_command('import_test_data')

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
