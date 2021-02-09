from django.test import TestCase

import modulesApplication.programmeInfo.factory as factory
from modulesApplication.models import Programme
from . import utils


class TestProgrammeInfo(TestCase):

    def setUp(self):
        utils.read_test_programmes()

    def test_programme_object(self):
        """Test that a new ProgrammeInfo is instantiated with the correct Programme object."""
        p = factory.get_programme_info(prog_code='1067')
        expected = Programme.objects.get(prog_code='1067')
        self.assertEqual(expected, p.programme)

    def test_stage(self):
        """Test that a new ProgrammeInfo object is given the correct number of stages"""

        # BSc Computer Science
        p = factory.get_programme_info(prog_code='1067')
        self.assertEqual(3, p.stages, "A standard BSc with no masters or YINI has three stages.")

        # BSc Computer Science (Year in Industry)
        p = factory.get_programme_info(prog_code='2327')
        self.assertEqual(4, p.stages, "A BSc with a YINI has 4 stages.")

        # MSCi Computer Science
        p = factory.get_programme_info(prog_code='2686')
        self.assertEqual(4, p.stages, "An MSCi with no YINI has 4 stages.")

        # MSCi Computer Science with YINI
        p = factory.get_programme_info(prog_code='2687')
        self.assertEqual(5, p.stages, "An MSCi with YINI has 5 stages.")