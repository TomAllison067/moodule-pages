from django.db import IntegrityError
from django.test import TestCase

from modulesApplication.models import CourseLeader, Module, People


class TestCourseLeader(TestCase):
    def setUp(self):
        self.professor = People.objects.create(id="TA", name="Tom Allison", email="foo@bar.com")
        self.module = Module.objects.create(mod_code="1234", title="How to write unit tests")

    def test_simple_course_leader(self):
        """Test simple functionality."""
        course_leader = CourseLeader(module=self.module, person=self.professor, leader=True, term="1")
        course_leader.save()
        self.assertEqual(1, CourseLeader.objects.count())

    def test_unique_together(self):
        """Tests that no CourseLeader objects can be created with the same module and professor twice."""
        CourseLeader.objects.create(module=self.module, person=self.professor, leader=True, term="1")
        with self.assertRaises(IntegrityError):
            CourseLeader.objects.create(module=self.module, person=self.professor, leader=False, term="2")


