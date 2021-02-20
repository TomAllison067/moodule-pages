from django.test import TestCase

from modulesApplication.models import Strands, Module


class TestQueries(TestCase):
    def test_db_strand_query(self):
        """
        Test to query and access values in the database
        """
        m = Module.objects.create(mod_code="fake")
        Strands.objects.create(module=m, strand='CM')
        self.assertEqual(1, Strands.objects.count(), "One strands added.")
        Strands(module=m,
                strand='HH').save()  # saving new strand object, total number of record should be 2
        self.assertEqual(2, Strands.objects.count(), "Two strands added.")
        new_module = Module.objects.create(mod_code='CS7432')  # new Module object
        third_strand = Strands(module=new_module, strand='CM')  # new stand object
        third_strand.save()  # saving a new strand from the new module, total records should be 3 now

        self.assertEqual(Strands.objects.count(), 3, 'added 3 strands to the database')
        # testing if the object entered is the same as the object in database
        self.assertEqual(Strands.objects.filter(module='CS7432').first(), third_strand)
        # test querying the database to get the strand value of a specific object
        self.assertEqual(Strands.objects.filter(module='CS7432').first().strand, 'CM')
