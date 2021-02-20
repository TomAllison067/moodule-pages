from django.test import TestCase

from modulesApplication.models import ModuleSelection, Programme
from modulesApplication.programmeInfo.selection_validator import SelectionValidator


class TestSelectionValidator(TestCase):
    def test_simple_selection_is_valid(self):
        programme = Programme.objects.create(prog_code="123", level="BSc")
        selection = ModuleSelection.objects.create(
            student_id="foo",
            stage="1",
            entry_year="2019",
            status="PENDING",
            programme=programme
        )
        # TODO: Add stub modules and have them selected by this validator
        pass

        # TODO: Add option rules linking stub programme to stub modules
        pass

        validator = SelectionValidator(selection)
        self.assertTrue(validator.validate(), "Not yet implemented.")
