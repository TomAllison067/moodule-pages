from django.core.exceptions import ValidationError
from django.test import TransactionTestCase

from modulesApplication.database.csv_reader import CsvReader
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

    def test_no_duplicates(self):
        """
        Test to check the database will not store duplicate values
        """
        self.newstrand.save()
        self.assertEqual(Strands.objects.count(), 1, "one record added ")
        same_strand = self.newstrand
        same_strand.save()  # trying to save same object
        self.assertEqual(Strands.objects.count(), 1, "if same record attempted to be inserted, it will not be added")

    def test_same_code_diff_strand(self):
        """
        Test so that modules can have multiple strands by having multiple records
        """
        self.newstrand.save()
        another_strand = Strands(mod_code=Module.objects.first(), strand='HH')
        another_strand.save()

        self.assertEqual(Strands.objects.count(), 2, "if there is 2 object with the same mod_code but different strand")
        self.assertNotEqual(Strands.objects.first().strand, Strands.objects.filter(mod_code='CS2815').last().strand)

    def test_db_query(self):
        """
        Test to query and access values in the database
        """
        self.newstrand.save()  # saving strand created in setup

        Strands(mod_code=Module.objects.first(), strand='HH').save()  # saving new strand object, total number of record should be 2

        new_module = Module(mod_code='CS7432')  # new Module object
        new_module.save()  # saving new Module
        third_strand = Strands(mod_code=new_module, strand='CM')  # new stand object
        third_strand.save()  # saving a new strand from the new module, total records should be 3 now

        self.assertEqual(Strands.objects.count(), 3, 'added 3 strands to the database')
        # testing if the object entered is the same as the object in database
        self.assertEqual(Strands.objects.filter(mod_code='CS7432').first(), third_strand)
        # test querying the database to get the strand value of a specific object
        self.assertEqual(Strands.objects.filter(mod_code='CS7432').first().strand, 'CM')

    def test_incorrect_mod_code(self):
        """
        Test to see if error thrown is the mod_code in not in Module database
        """
        module = Module(mod_code='HS234')
        #self.assertRaises(ValidationError, Strands(mod_code=module, strand='HS').save)

    def test_read_from_csv_and_save_to_database(self):
        Module.objects.all().delete()
        Strands.objects.all().delete()

        cr = CsvReader()
        modules = cr.read_table("modulesApplication/tests/resources/exported_sqlite3_module_table.csv",
                                Module)
        for m in modules:
            m.clean()
        Module.objects.bulk_create(modules)
        print(Module.objects.count())

        csv_strands = cr.read_table("modulesApplication/tests/resources/exported_strands_table.csv", Strands)
        self.assertEqual(42, len(csv_strands), "There are 42 strands in the csv file.")

        for s in csv_strands:
            s.clean()
        for stra in csv_strands:
            stra.save()
        self.assertEqual(40, Strands.objects.count(), "There are 40 strands in the database. 2 mod_code unfound.")
        for cstrand in Strands.objects.all():
            print(cstrand.mod_code, cstrand.strand, cstrand.strand_id)
