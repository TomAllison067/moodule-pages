from django.test import TestCase, tag

from modulesApplication.models import ModuleSelection, Module


@tag('unit')
class TestModuleSelection(TestCase):
    def test_simple_selection(self):
        selection = ModuleSelection.objects.create(student_id='1234', stage='1', status='PENDING')
        self.assertEqual('1234', selection.student_id)
        self.assertEqual('1', selection.stage)
        self.assertEqual('PENDING', selection.status)

    def test_modules(self):
        selection = ModuleSelection.objects.create(student_id='1234', stage='1', status='PENDING')
        m1 = Module.objects.create(mod_code='cs1234', title='foo')
        m2 = Module.objects.create(mod_code='cs4567', title='bar')
        m1.selected_in.add(selection)
        m2.selected_in.add(selection)
        selected = selection.module_set.all()
        self.assertEqual(set(Module.objects.all()), set(selected))
