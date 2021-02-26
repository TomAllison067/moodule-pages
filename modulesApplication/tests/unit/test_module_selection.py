from django.test import TestCase, tag

from modulesApplication.models import ModuleSelection, Module, Programme


@tag('unit')
class TestModuleSelection(TestCase):
    def setUp(self):
        self.p = Programme.objects.create(prog_code="foo", level="BSc")
        self.selection = ModuleSelection.objects.create(
            student_id='1234', stage='1', status='PENDING', programme=self.p)

    def test_simple_selection(self):
        self.assertEqual('1234', self.selection.student_id)
        self.assertEqual('1', self.selection.stage)
        self.assertEqual('PENDING', self.selection.status)

    def test_modules(self):
        m1 = Module.objects.create(mod_code='cs1234', title='foo')
        m2 = Module.objects.create(mod_code='cs4567', title='bar')
        m1.selected_in.add(self.selection)
        m2.selected_in.add(self.selection)
        selected = self.selection.module_set.all()
        self.assertEqual(set(Module.objects.all()), set(selected))
