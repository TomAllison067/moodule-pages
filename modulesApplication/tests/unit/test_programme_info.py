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

    def test_entry_year(self):
        """Test that a new ProgrammeInfo object has the correct entry year."""
        p = Programme.objects.create(prog_code='madeup', level='BSc')
        p = factory.get_programme_info(prog_code='madeup', entry_year='2019')
        expected = '2019'
        self.assertEqual(expected, p.entry_year)
