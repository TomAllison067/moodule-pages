from django.test import TestCase
from modulesApplication.models import CourseLeader, Module, People


class TestCourseLeader(TestCase):
    def test_simple_course_leader(self):
        professor = People.objects.create(id="TA", name="Tom Allison", email="foo@bar.com")
        module = Module.objects.create(mod_code="1234", title="How to write unit tests")
        course_leader = CourseLeader(module=module, person=professor, leader=True, term="1")
        course_leader.save()
        self.assertEqual(1, CourseLeader.objects.count())
