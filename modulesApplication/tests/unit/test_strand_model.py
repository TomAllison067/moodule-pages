from django.test import TestCase, tag

from modulesApplication.models import Strands, Module


@tag('unit')
class TestStrandModel(TestCase):

    def test_empty(self):
        """
        Test to check there are no Strands in the database
        """
        self.assertFalse(Strands.objects.exists(), "There are no objects hence returns empty list")

    def test_add_strand(self):
        """
        Test to insert a new object into the database
        """
        m = Module.objects.create(mod_code="CS2815", title="Small Enterprise Team Project", level=4)
        newstrand = Strands.objects.create(module=m, strand='SE')
        newstrand.save()
        self.assertEqual(Strands.objects.count(), 1, "Strand added to database, total number of records should be 1")

    def test_no_duplicates(self):
        """
        Test to check the database will not store duplicate values
        """
        m = Module.objects.create(mod_code="CS2815", title="Small Enterprise Team Project", level=4)
        newstrand = Strands.objects.create(module=m, strand='SE')
        self.assertEqual(Strands.objects.count(), 1, "one record added ")
        same_strand = newstrand
        same_strand.save()  # trying to save same object
        self.assertEqual(Strands.objects.count(), 1, "if same record attempted to be inserted, it will not be added")

    def test_same_code_diff_strand(self):
        """
        Test so that modules can have multiple strands by having multiple records
        """
        m = Module.objects.create(mod_code="CS2815", title="Small Enterprise Team Project", level=4)
        newstrand = Strands.objects.create(module=m, strand='SE')
        self.assertEqual(Strands.objects.count(), 1, "one record added ")
        another_strand = Strands(module=m, strand='AI')
        another_strand.save()

        self.assertEqual(Strands.objects.count(), 2, "if there is 2 object with the same module but different strand")
        self.assertNotEqual(Strands.objects.first().strand, Strands.objects.filter(module='CS2815').last().strand)
