from django.db.models import Q
from django.test import TransactionTestCase, TestCase

import modulesApplication.programmeInfo.factory as factory
from modulesApplication.models import Programme, Module, OptionRule
from . import utils


class TestProgrammeInfo(TestCase):

    @classmethod
    def setUpClass(cls):
        utils.read_test_programmes()
        utils.read_test_optionrules()
        utils.read_test_modules()
        utils.read_optional_modules()
        super(TestProgrammeInfo, cls).setUpClass()

    def test_programme_object(self):
        """Test that a new ProgrammeInfo is instantiated with the correct Programme object."""
        p = factory.get_programme_info(prog_code='1067', entry_year='2019')
        expected = Programme.objects.get(prog_code='1067')
        self.assertEqual(expected, p.programme)

    def test_stage(self):
        """Test that a new ProgrammeInfo object is given the correct number of stages"""

        # BSc Computer Science
        p = factory.get_programme_info(prog_code='1067', entry_year='2019')
        self.assertEqual(3, p.stages, "A standard BSc with no masters or YINI has three stages.")

        # BSc Computer Science (Year in Industry)
        p = factory.get_programme_info(prog_code='2327', entry_year='2019')
        self.assertEqual(4, p.stages, "A BSc with a YINI has 4 stages.")

        # MSCi Computer Science
        p = factory.get_programme_info(prog_code='2686', entry_year='2019')
        self.assertEqual(4, p.stages, "An MSCi with no YINI has 4 stages.")

        # MSCi Computer Science with YINI
        p = factory.get_programme_info(prog_code='2687', entry_year='2019')
        self.assertEqual(5, p.stages, "An MSCi with YINI has 5 stages.")

    def test_entry_year(self):
        """Test that a new ProgrammeInfo object has the correct entry year."""
        p = factory.get_programme_info(prog_code='1067', entry_year='2019')
        expected = '2019'
        self.assertEqual(expected, p.entry_year)

    # TODO fix the tests... i know this is bad!

    # def test_core_modules(self):
    #     """Tests that a new ProgrammeInfo object has the correct stage 1 modules."""
    #     p = factory.get_programme_info(prog_code='1067', entry_year='2019')
    #     stage1_patterns = {'CORE': ['CS1811', 'CS1840', 'CS1860', 'CS1870', 'CS1890']}
    #     stage1_modules = {'CORE': [Module.objects.get(pk=mc) for mc in stage1_patterns['CORE']]}
    #     self.assertEqual(stage1_modules['CORE'], p.get_modules(stage=1)['CORE'])
    #
    #     stage2_patterns = {'CORE': ['CS2800', 'CS2810', 'CS2850', 'CS2855', 'CS2860', 'IY2760']}
    #     stage2_modules = {'CORE': [Module.objects.get(pk=mc) for mc in stage2_patterns['CORE']]}
    #     self.assertEqual(stage2_modules['CORE'], p.get_modules(stage=2)['CORE'])
    #
    #     stage3_patterns = {'CORE': ['CS3821']}
    #     stage3_modules = {'CORE': [Module.objects.get(pk=mc) for mc in stage3_patterns['CORE']]}
    #     self.assertEqual(stage3_modules['CORE'], p.get_modules(stage=3)['CORE'])
    #
    # def test_disc_alt_modules(self):
    #     """Test that a new ProgrammeInfo object has the correct discretionary alternative modules,
    #     available in stage 1 only."""
    #     p = factory.get_programme_info(prog_code='1067', entry_year='2019')
    #     stage1_patterns = {'DISC_ALT': ['CS1812,CS1813', 'CS1822,CS1821']}
    #     stage1_modules = {'DISC_ALT': [[Module.objects.get(mod_code=mc) for mc in pattern.split(",")]
    #                                    for pattern in stage1_patterns['DISC_ALT']]}
    #     self.assertEqual(stage1_modules['DISC_ALT'], p.get_modules(stage=1)['DISC_ALT'])
    #
    # def test_optional_modules(self):
    #     """
    #     Tests a ProgrammeInfo has the correct optional modules. Correct optional modules are those that match
    #     the relevant OptionRule mod_code_pattern AND are matched in the OptionalModules table.
    #     Only applies to stage 2 upwards.
    #     """
    #
    #     # BSc Computer Science with YINI
    #     p = factory.get_programme_info(prog_code='2327', entry_year='2019')
    #     expected1 = {Module.objects.get(pk='CS2900'), Module.objects.get(pk='CS2910'), Module.objects.get(pk='IY2840')}
    #     self.assertEqual(expected1, set(p.get_modules(stage=2)['OPTS']))  # Year 2
    #
    #     expected2_modcodes = ['IY3840',
    #                           'IY3606', 'CS3940', 'CS3945', 'CS3470', 'IY3660', 'CS3840', 'CS3110', 'CS3846', 'IY3612',
    #                           'CS3510', 'IY3501', 'CS3220', 'IY3609', 'CS3750', 'CS3003', 'CS3930', 'CS3000', 'CS3480',
    #                           'CS3870', 'CS3490', 'CS3250', 'CS3580', 'CS3920']
    #     expected2 = set([Module.objects.get(pk=m) for m in expected2_modcodes])
    #     self.assertEqual(expected2, set(p.get_modules(stage=4)['OPTS']))  # Year 3 (2327 has YINI for stage 2)
    #
    #     # MSCi Computer Science - Stage 4
    #     p = factory.get_programme_info(prog_code='2686', entry_year='2019')
    #     expected3_modcodes = ['CS4860', 'CS4915', 'CS4870', 'IY4523', 'CS4580', 'IY4606', 'IY4609', 'CS4234', 'CS4220',
    #                           'IY4612', 'CS4490', 'CS4250', 'CS4945', 'CS4563', 'CS4920', 'CS4990', 'CS4950', 'CS4504',
    #                           'CS4200', 'CS4100', 'IY4501', 'IY4610', 'CS4980', 'CS4910']
    #     expected3 = set([Module.objects.get(pk=m) for m in expected3_modcodes])
    #     self.assertEqual(expected3, set(p.get_modules(stage=4)['OPTS']))
    #
    # def test_strand_modules(self):
    #     """
    #     Tests a ProgrammeInfo has the correct optional modules corresponding to a certain strand.
    #     """
    #     # MSCi Computer Science (Artifical Intelligence) with YINI
    #     p = factory.get_programme_info(prog_code='2674', entry_year='2019')
    #     expected1 = set([m for m in Module.objects.filter(mod_code__startswith='CS2', strands__strand='AI')])
    #     expected2 = set([m for m in
    #                      Module.objects.filter(
    #                          Q(strands__strand='AI') &
    #                          (Q(mod_code__startswith='CS3') |
    #                           Q(mod_code__startswith='IY3'))
    #                      )])
    #     expected3 = set([m for m in
    #                      Module.objects.filter(
    #                          Q(strands__strand='AI') &
    #                          (Q(mod_code__startswith='CS4') |
    #                           Q(mod_code__startswith='IY4'))
    #                      )])
    #     self.assertEqual(expected1, set(p.get_modules(stage=2)['STRAND']))
    #     self.assertEqual(expected2, set(p.get_modules(stage=3)['STRAND']))
    #     self.assertEqual(expected3, set(p.get_modules(stage=5)['STRAND']))
