from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TransactionTestCase

from modulesApplication.database.csv_reader import CsvReader
from modulesApplication.models import Module


class TestModulesModel(TransactionTestCase):
    def setUp(self):
        self.module1 = Module(mod_code="CS2815", title="Small Enterprise Team Project", level=2, department="CS")

    def test_no_module(self):
        """
        Tests that no modules exist in a new, empty database.
        """
        q = Module.objects.filter(pk="CS2815")
        self.assertEqual(q.count(), 0, "There should be no models in the database until one is saved.")

    def test_new_module(self):
        """
        Tests that a new module can be created, saved in the database, and then queried.
        """
        m = Module(mod_code="foobar", title="baz")
        m.save()
        q = Module.objects.get(pk="foobar")
        self.assertIsNotNone(q, "The newly created Module object is null.")
        self.assertEqual("foobar", q.mod_code)

    def test_no_mod_code_throws_value_error(self):
        """
        Tests that constructing a new module with Module.objects.create throws a value error, and that calling save()
        on a new regularly instantiated object does the same
        """
        self.assertRaises(ValueError, Module.objects.create, mod_code=None)
        self.assertRaises(ValueError, Module.objects.create, mod_code="")
        self.module1.mod_code = None
        self.assertRaises(ValueError, self.module1.save)
        self.module1.mod_code = ""
        self.assertRaises(ValueError, self.module1.save)
        self.module1.mod_code = "CS2800"
        self.module1.save()
        self.assertEqual(self.module1, Module.objects.filter(pk="CS2800").first())

    def test_no_duplicate_modules(self):
        """
        Tests that two modules with the same primary key cannot be put into the database.
        """
        Module.objects.create(mod_code="foo")  # Create the initial module
        self.assertRaises(ValidationError, Module.objects.create, mod_code="foo")  # Test the create method
        m2 = Module(mod_code="foo")
        self.assertRaises(ValidationError, m2.save, force_insert=True)  # Test the save method

    def test_read_from_csv_and_save_to_database(self):
        cr = CsvReader()
        modules = cr.read_table("modulesApplication/tests/resources/exported_sqlite3_module_table.csv",
                                Module)
        self.assertEqual(113, len(modules), "There are 113 modules in the csv file.")
        for m in modules:
            m.clean()
        Module.objects.bulk_create(modules)
        self.assertEqual(113, Module.objects.count(), "There are 113 modules in the database.")