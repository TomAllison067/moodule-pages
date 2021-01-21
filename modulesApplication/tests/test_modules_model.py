from django.test import TestCase

from modulesApplication.models import Module


class TestModulesModel(TestCase):
    def setUp(self):
        self.module1 = Module(mod_code="CS2815", title="Small Enterprise Team Project", year=2, department="CS",
                              contact_hours=40, exams=0, practical=0, coursework=100, credits=15,
                              prerequisites="CS1813; CS2800", summary="This is a test summary",
                              outcomes="To do TDD in our project", status="ACTIVE")

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
