from django.test import TestCase, tag

from modulesApplication.models import ModuleSelection, Programme, Module, OptionRule, Strands
from modulesApplication.programmeInfo.selection_validator import SelectionValidator


@tag('unit')
class TestSelectionValidator(TestCase):
    def setUp(self):
        self.p1 = Programme.objects.create(prog_code="p1", level="BSc")
        self.selection = selection = ModuleSelection.objects.create(
            student_id="foo",
            stage=1,
            entry_year="2019",
            status="PENDING",
            programme=self.p1
        )

    def test_simple_selection_is_valid(self):
        """Assert that a simple made up stage 1 selection is correct - i.e, core modules."""
        # Add stub modules and have them selected by this validator
        cm1 = Module.objects.create(mod_code="m1", title="module1")
        cm2 = Module.objects.create(mod_code="m2", title="module2")

        # Add option rules linking stub programme to stub modules
        OptionRule.objects.create(
            prog_code=self.p1,
            entry_year='2019',
            stage=1,
            constraint_type="CORE",
            min_quantity=2,
            max_quantity=2,
            mod_code_pattern="m1,m2"
        )

        # The valid selection contains both core modules.
        cm1.selected_in.add(self.selection)
        cm2.selected_in.add(self.selection)

        self.assertTrue(SelectionValidator(self.selection).validate(), "A valid selection should return True.")

        cm2.selected_in.remove(self.selection)
        self.assertFalse(SelectionValidator(self.selection).validate(), "An invalid selection should return False.")

    def test_simple_selection_with_disc_alts(self):
        """Test a selection in stage 1 with disc_alt modules is valid/invalid"""
        core_m1 = Module.objects.create(mod_code="core_m1", title="module1")
        alt_m1 = Module.objects.create(mod_code="alt_m1", title="alt module1")
        alt_m2 = Module.objects.create(mod_code="alt_m2", title="disc alt to alt module1")

        # Create the core rule
        OptionRule.objects.create(
            prog_code=self.p1,
            entry_year='2019',
            stage=1,
            constraint_type="CORE",
            min_quantity=1,
            max_quantity=1,
            mod_code_pattern="core_m1"
        )

        # Create the disc_alt rule
        OptionRule.objects.create(
            prog_code=self.p1,
            entry_year='2019',
            stage=1,
            constraint_type="DISC_ALT",
            min_quantity=1,
            max_quantity=1,
            mod_code_pattern="alt_m1,alt_m2"
        )

        core_m1.selected_in.add(self.selection)
        alt_m1.selected_in.add(self.selection)

        # Test that a selection with only the first of the DISC_ALT modules is valid.
        self.assertTrue(SelectionValidator(self.selection).validate(),
                        "A selection with only core modules and the first of DISC_ALT should return true.")

        # Test that a selection with only the second of the DISC_ALT modules is valid.
        alt_m1.selected_in.remove(self.selection)
        alt_m2.selected_in.add(self.selection)
        self.assertTrue(SelectionValidator(self.selection).validate(),
                        "A selection with only core modules and the second of DISC_ALT should return true.")

        # Test that a selection with both of the DISC_ALT modules is invalid.
        alt_m1.selected_in.add(self.selection)
        self.assertFalse(SelectionValidator(self.selection).validate(),
                         "A selection with core modules but both of DISC_ALT should return False.")

    def test_simple_strand_selection(self):
        """Tests the Strand OptionRules. This test covers STRAND modules without any OPTS patterns, i.e., stage 2.
        Stage 3 & beyond may have crossover between OPTS and STRAND modules, which is covered in later tests."""
        ai1 = Module.objects.create(mod_code="cs21", title="Artificial Intelligence")
        ai2 = Module.objects.create(mod_code="cs22", title="Artificial Unintelligence")
        ai3 = Module.objects.create(mod_code="iy23", title="Artificial Redundancy")
        Strands.objects.create(module=ai1, strand="AI")
        Strands.objects.create(module=ai2, strand="AI")
        Strands.objects.create(module=ai3, strand="AI")
        OptionRule.objects.create(
            prog_code=self.p1, mod_code_pattern="AI,cs2,iy2", constraint_type="STRAND", stage=1, entry_year='2019',
            min_quantity=2, max_quantity=2)
        ai1.selected_in.add(self.selection)
        self.assertFalse(SelectionValidator(self.selection).validate(),
                         "A selection with too few strand modules is valid.")
        ai2.selected_in.add(self.selection)
        self.assertTrue(SelectionValidator(self.selection).validate(),
                        "A selection with the correct number of strand modules is valid.")
        ai3.selected_in.add(self.selection)
        self.assertFalse(SelectionValidator(self.selection).validate(),
                         "A selection with too many strand modules is invalid.")

    def test_simple_opts_selection(self):
        """Tests that a selection of simple OPTS modules is correct, not considering any STRANDS that may overlap."""
        opts1 = Module.objects.create(mod_code="cs21", title="Optional Science")
        opts2 = Module.objects.create(mod_code="cs22", title="Optional Mathematics")
        opts3 = Module.objects.create(mod_code="iy23", title="Optional WhateverYouFeelLikeStudying")
        OptionRule.objects.create(
            prog_code=self.p1, mod_code_pattern="cs2,iy2", constraint_type="OPTS", stage=1, entry_year='2019',
            min_quantity=2, max_quantity=2)

        opts1.selected_in.add(self.selection)
        self.assertFalse(SelectionValidator(self.selection).validate(),
                         "A selection with too few OPTS modules is valid.")
        opts2.selected_in.add(self.selection)
        self.assertTrue(SelectionValidator(self.selection).validate(),
                        "A selection with the correct number of OPTS modules is valid.")
        opts3.selected_in.add(self.selection)
        self.assertFalse(SelectionValidator(self.selection).validate(),
                         "A selection with too many OPTS modules is invalid.")
