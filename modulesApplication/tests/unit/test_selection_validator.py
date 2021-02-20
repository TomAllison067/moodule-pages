from django.test import TestCase

from modulesApplication.models import ModuleSelection


class TestSelectionValidator(TestCase):
    def test_simple_selection_is_valid(self):
        selection = ModuleSelection
