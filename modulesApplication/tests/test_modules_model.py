from django.db.utils import IntegrityError
from django.test import TransactionTestCase

from modulesApplication.database.models import Module


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
        m = self.module1
        m.save()
        q = Module.objects.filter(pk="CS2815").first()
        self.assertIsNotNone(q, "The newly created Module object is null.")
        self.assertEqual("CS2815", q.mod_code)

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
        self.assertRaises(IntegrityError, Module.objects.create, mod_code="foo")  # Test the create method
        m2 = Module(mod_code="foo")
        self.assertRaises(IntegrityError, m2.save, force_insert=True)  # Test the save method
