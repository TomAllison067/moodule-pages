from django.test import TestCase

from modulesApplication.models import Strands, Module


class TestQueries(TestCase):
    def test_db_strand_query(self):
        """
        Test to query and access values in the database
        """
        newstrand = Strands.objects.create(module=Module.objects.first(), strand='CM')

        Strands(module=Module.objects.first(),
                strand='HH').save()  # saving new strand object, total number of record should be 2

        new_module = Module(mod_code='CS7432')  # new Module object
        new_module.save()  # saving new Module
        third_strand = Strands(module=new_module, strand='CM')  # new stand object
        third_strand.save()  # saving a new strand from the new module, total records should be 3 now

        self.assertEqual(Strands.objects.count(), 3, 'added 3 strands to the database')
        # testing if the object entered is the same as the object in database
        self.assertEqual(Strands.objects.filter(module='CS7432').first(), third_strand)
        # test querying the database to get the strand value of a specific object
        self.assertEqual(Strands.objects.filter(module='CS7432').first().strand, 'CM')
