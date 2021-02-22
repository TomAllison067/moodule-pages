from django.test import TestCase, tag

from modulesApplication.models import ModuleSelection, Programme, Module, OptionRule
from modulesApplication.programmeInfo.selection_validator import SelectionValidator


@tag('unit')
class TestSelectionValidator(TestCase):
    def test_simple_selection_is_valid(self):
        """Assert that a simple made up stage 1 selection is correct - i.e, core modules."""
        p1 = Programme.objects.create(prog_code="p1", level="BSc")
        valid_selection = ModuleSelection.objects.create(
            student_id="foo",
            stage=1,
            entry_year="2019",
            status="PENDING",
            programme=p1
        )
        invalid_selection = ModuleSelection.objects.create(
            student_id="bar",
            stage="1",
            entry_year="2019",
            status="PENDING",
            programme=p1
        )
        # Add stub modules and have them selected by this validator
        cm1 = Module.objects.create(mod_code="m1", title="module1")
        cm2 = Module.objects.create(mod_code="m2", title="module2")

        # Add option rules linking stub programme to stub modules
        OptionRule.objects.create(
            prog_code=p1,
            entry_year='2019',
            stage=1,
            constraint_type="CORE",
            min_quantity=2,
            max_quantity=2,
            mod_code_pattern="m1,m2"
        )

        # The valid selection contains both core modules.
        cm1.selected_in.add(valid_selection)
        cm2.selected_in.add(valid_selection)

        # The invalid selection contains only one of the core modules.
        validator = SelectionValidator(valid_selection)
        self.assertTrue(validator.validate(), "A valid selection should return True.")

        validator = SelectionValidator(invalid_selection)
        self.assertFalse(validator.validate(), "An invalid selection should return False.")

    def test_simple_selection_with_disc_alts(self):
        p1 = Programme.objects.create(prog_code="p1", level="BSc")

        """Test a selection in stage 1 with disc_alt modules is valid/invalid"""
        core_m1 = Module.objects.create(mod_code="core_m1", title="module1")
        alt_m1 = Module.objects.create(mod_code="alt_m1", title="alt module1")
        alt_m2 = Module.objects.create(mod_code="alt_m2", title="disc alt to alt module1")

        # Create the core rule
        OptionRule.objects.create(
            prog_code=p1,
            entry_year='2019',
            stage=1,
            constraint_type="CORE",
            min_quantity=1,
            max_quantity=1,
            mod_code_pattern="core_m1"
        )

        # Create the disc_alt rule
        OptionRule.objects.create(
            prog_code=p1,
            entry_year='2019',
            stage=1,
            constraint_type="DISC_ALT",
            min_quantity=1,
            max_quantity=1,
            mod_code_pattern="alt_m1,alt_m2"
        )

        selection = ModuleSelection.objects.create(
            student_id="foo",
            stage=1,
            entry_year="2019",
            status="PENDING",
            programme=p1
        )
        core_m1.selected_in.add(selection)
        alt_m1.selected_in.add(selection)

        # Test that a selection with only the first of the DISC_ALT modules is valid.
        self.assertTrue(SelectionValidator(selection).validate(),
                        "A selection with only core modules and the first of DISC_ALT should return true.")

        # Test that a selection with only the second of the DISC_ALT modules is valid.
        alt_m1.selected_in.remove(selection)
        alt_m2.selected_in.add(selection)
        self.assertTrue(SelectionValidator(selection).validate(),
                        "A selection with only core modules and the second of DISC_ALT should return true.")

        # Test that a selection with both of the DISC_ALT modules is invalid.
        alt_m1.selected_in.add(selection)
        self.assertFalse(SelectionValidator(selection).validate(),
                         "A selection with core modules but both of DISC_ALT should return False.")
