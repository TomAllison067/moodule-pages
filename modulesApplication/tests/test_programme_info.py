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

    def test_core_modules(self):
        """Tests that a new ProgrammeInfo object has the correct stage 1 modules."""
        p = factory.get_programme_info(prog_code='1067', entry_year='2019')
        stage1_patterns = {'CORE': ['CS1811', 'CS1840', 'CS1860', 'CS1870', 'CS1890']}
        stage1_modules = {'CORE': [Module.objects.get(pk=mc) for mc in stage1_patterns['CORE']]}
        self.assertEqual(stage1_modules['CORE'], p.get_modules(stage=1)['CORE'])

        stage2_patterns = {'CORE': ['CS2800', 'CS2810', 'CS2850', 'CS2855', 'CS2860', 'IY2760']}
        stage2_modules = {'CORE': [Module.objects.get(pk=mc) for mc in stage2_patterns['CORE']]}
        self.assertEqual(stage2_modules['CORE'], p.get_modules(stage=2)['CORE'])

        stage3_patterns = {'CORE': ['CS3821']}
        stage3_modules = {'CORE': [Module.objects.get(pk=mc) for mc in stage3_patterns['CORE']]}
        self.assertEqual(stage3_modules['CORE'], p.get_modules(stage=3)['CORE'])

    # @classmethod
    # def tearDownClass(cls):
    #     Programme.objects.all().delete()
    #     Module.objects.all().delete()
    #     OptionRule.objects.all().delete()
    #     super(TestProgrammeInfo, cls).tearDownClass()
