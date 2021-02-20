from django.core.exceptions import ValidationError
from django.test import TransactionTestCase

from modulesApplication.models import Module


class TestModulesModel(TransactionTestCase):

    def test_no_mod_code_throws_value_error(self):
        """
        Tests that constructing a new module with Module.objects.create throws a value error, and that calling save()
        on a new regularly instantiated object does the same
        """
        self.assertRaises(ValueError, Module.objects.create, mod_code=None)
        self.assertRaises(ValueError, Module.objects.create, mod_code="")

    def test_no_duplicate_modules(self):
        """
        Tests that two modules with the same primary key cannot be put into the database.
        """
        Module.objects.create(mod_code="foo")  # Create the initial module
        self.assertRaises(ValidationError, Module.objects.create, mod_code="foo")  # Create it again
        m2 = Module(mod_code="foo")
        self.assertRaises(ValidationError, m2.save, force_insert=True)  # Test the save method
