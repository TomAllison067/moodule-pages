from django.db import IntegrityError
from django.test import TestCase, tag

from modulesApplication.models import People


@tag('unit')
class TestPeople(TestCase):
    def test_simple_person(self):
        """Test simple functionality."""
        People.objects.create(id="TA", name="Tom Allison", email="foo@bar.com")
        self.assertEqual(1, People.objects.count())

    def test_no_duplicate_pk(self):
        """Test that no duplicate primary keys can be saved (the initials)."""
        People.objects.create(id="TA", name="Tom Allison", email="foo@bar.com")
        with self.assertRaises(IntegrityError):
            People.objects.create(id="TA", name="Tim Allinson", email="foo@bar.com")
            self.fail("Integrity error not raised on duplicate PK.")
