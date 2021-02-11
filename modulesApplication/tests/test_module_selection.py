from django.test import TestCase

from modulesApplication.models import ModuleSelection


class TestModuleSelection(TestCase):
    def test_simple_selection(self):
        selection = ModuleSelection.objects.create(student_id='1234', stage='1', status='PENDING')
        self.assertEqual(1, selection.id)
        self.assertEqual('1234', selection.student_id)
        self.assertEqual('1', selection.stage)
        self.assertEqual('PENDING', selection.status)
