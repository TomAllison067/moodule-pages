from django.test import TestCase

from modulesApplication.models import Module


class TestModulesModel(TestCase):
    def test_new_module(self):
        """
        Tests that a new module can be created, saved in the database, and then queried.
        """
        m = Module(mod_code="CS2815", title="Small Enterprise Team Project", year=2, department="CS",
                   contact_hours=40, exams=0, practical=0, coursework=100, credits=15,
                   prerequisites="CS1813; CS2800", summary="This is a test summary",
                   outcomes="To do TDD in our project", status="ACTIVE")
        m.save()
        m1 = Module.objects.filter(pk="CS2815").first()
        self.assertIsNotNone(m1, "The newly created Module object is null.")
        self.assertEqual("CS2815", m1.mod_code)
