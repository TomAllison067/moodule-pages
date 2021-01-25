from django.test import TransactionTestCase
from modulesApplication.models import Strands, Module


class MyTestCase(TransactionTestCase):
    def setUp(self):
        m = Module(mod_code="CS2815", title="Small Enterprise Team Project", level=2, department="CS")
        m.save()
        self.newstrand = Strands(mod_code=Module.objects.first(), strand='CM')

    def test_empty(self):
        """
        Test to check there are no Strands in the database
        """
        self.assertFalse(Strands.objects.exists(), "There are no objects hence returns empty list")

    def test_add_strand(self):
        """
        Test to insert a new object into the database
        """
        self.newstrand.save()
        self.assertEqual(Strands.objects.count(), 1, "Strand added to database, total number of records should be 1")

    def test_duplicates(self):
        """
        Test if database will store duplicate values
        """
        self.newstrand.save()
        self.assertEqual(Strands.objects.count(), 1, "one record added ")
        same_strand = self.newstrand
        same_strand.save()
        self.assertEqual(Strands.objects.count(), 1, "if same record attempted to be inserted, it will not be added")



