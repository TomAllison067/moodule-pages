from django.db import IntegrityError
from django.test import TestCase

from modulesApplication.models import People


class TestPeople(TestCase):
    def test_simple_person(self):
        People.objects.create(id="TA", name="Tom Allison", email="foo@bar.com")
        self.assertEqual(1, People.objects.count())

    def test_no_duplicate_pk(self):
        People.objects.create(id="TA", name="Tom Allison", email="foo@bar.com")
        with self.assertRaises(IntegrityError):
            People.objects.create(id="TA", name="Tim Allinson", email="foo@bar.com")
            self.fail("Integrity error not raised on duplicate PK.")