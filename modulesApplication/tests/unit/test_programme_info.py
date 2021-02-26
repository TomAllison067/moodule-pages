from django.test import TestCase, tag

import modulesApplication.programmeInfo.factory as factory
from modulesApplication.models import Programme


@tag('unit', 'slow')
class TestProgrammeInfo(TestCase):
    """
    A class to test the ProgrammeInfo object and whether it is created proprely by its factory.
    """

    def test_programme_object(self):
        """Test that a new ProgrammeInfo is instantiated with the correct Programme object."""
        programme = Programme.objects.create(prog_code='foo', level='bsc')
        p = factory.get_programme_info(prog_code='foo', entry_year='2019')
        expected = Programme.objects.get(prog_code='foo')
        self.assertEqual(expected, p.programme)

    def test_stage(self):
        """Test that a new ProgrammeInfo object is given the correct number of stages"""

        # BSc
        bsc = Programme.objects.create(prog_code='bsc', title='bsc', level='BSc', yini=0)
        p = factory.get_programme_info(prog_code='bsc', entry_year='2019')
        self.assertEqual(3, p.stages, "A standard BSc with no masters or YINI has three stages.")

        # BSc (Year in Industry)
        bsc_yini = Programme.objects.create(prog_code='bscyini', title='bscyini', level='BSc', yini=1)
        p = factory.get_programme_info(prog_code='bscyini', entry_year='2019')
        self.assertEqual(4, p.stages, "A BSc with a YINI has 4 stages.")

        # MSCi
        msci = Programme.objects.create(prog_code='msci', title='msci', level='msci', yini=0)
        p = factory.get_programme_info(prog_code='msci', entry_year='2019')
        self.assertEqual(4, p.stages, "An MSCi with no YINI has 4 stages.")

        # MSCi YINI
        msci_yini = Programme.objects.create(prog_code='msciyini', title='msciyini', level='msci', yini=1)
        p = factory.get_programme_info(prog_code='msciyini', entry_year='2019')
        self.assertEqual(5, p.stages, "An MSCi with YINI has 5 stages.")

    def test_entry_year(self):
        """Test that a new ProgrammeInfo object has the correct entry year."""
        p = Programme.objects.create(prog_code='madeup', level='BSc')
        p = factory.get_programme_info(prog_code='madeup', entry_year='2019')
        expected = '2019'
        self.assertEqual(expected, p.entry_year)
