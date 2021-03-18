from django.test import TestCase, tag

from modulesApplication.models import Programme, Module, OptionRule, Strands
from modulesApplication.programmeInfo.selection_validator import SelectionValidator


@tag('unit')
class TestSelectionValidator(TestCase):
    entry_year = '2019'
    stage = '1'

    def setUp(self):
        self.p1 = Programme.objects.create(prog_code="p1", level="BSc")
        self.prog_code = self.p1.prog_code

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
        mod_codes = {cm1.mod_code, cm2.mod_code}

        self.assertTrue(SelectionValidator(prog_code=self.prog_code, stage=self.stage, mod_codes=mod_codes,
                                           entry_year=self.entry_year).validate(),
                        "A valid selection should return True.")

        mod_codes.remove(cm2.mod_code)
        self.assertFalse(SelectionValidator(prog_code=self.prog_code, stage=self.stage, mod_codes=mod_codes,
                                            entry_year=self.entry_year).validate(),
                         "An invalid selection should return False.")

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

        mod_codes = {core_m1.mod_code, alt_m1.mod_code}
        # Test that a selection with only the first of the DISC_ALT modules is valid.
        self.assertTrue(SelectionValidator(prog_code=self.prog_code, stage=self.stage, mod_codes=mod_codes,
                                           entry_year=self.entry_year).validate(),
                        "A selection with only core modules and the first of DISC_ALT should return true.")

        # Test that a selection with only the second of the DISC_ALT modules is valid.
        mod_codes.remove(alt_m1.mod_code)
        mod_codes.add(alt_m2.mod_code)
        self.assertTrue(SelectionValidator(prog_code=self.prog_code, stage=self.stage, mod_codes=mod_codes,
                                           entry_year=self.entry_year).validate(),
                        "A selection with only core modules and the second of DISC_ALT should return true.")

        # Test that a selection with both of the DISC_ALT modules is invalid.
        mod_codes.add(alt_m1.mod_code)
        self.assertFalse(SelectionValidator(prog_code=self.prog_code, stage=self.stage, mod_codes=mod_codes,
                                            entry_year=self.entry_year).validate(),
                         "A selection with core modules but both of DISC_ALT should return False.")

    def test_strand_selection(self):
        """Tests the Strand OptionRules. This test begins with a simple selection of only STRANDS modules,
        and then tests whether extra STRAND modules can successfully 'spill over' into OPTS."""
        ai1 = Module.objects.create(mod_code="cs21", title="Artificial Intelligence")
        ai2 = Module.objects.create(mod_code="cs22", title="Artificial Unintelligence")
        ai3 = Module.objects.create(mod_code="iy23", title="Artificial Redundancy")
        Strands.objects.create(module=ai1, strand="AI")
        Strands.objects.create(module=ai2, strand="AI")
        Strands.objects.create(module=ai3, strand="AI")
        OptionRule.objects.create(
            prog_code=self.p1, mod_code_pattern="AI,cs2,iy2", constraint_type="STRAND", stage=1, entry_year='2019',
            min_quantity=2, max_quantity=2)
        mod_codes = {ai1.mod_code}

        # Not selecting enough STRAND modules should return False.
        self.assertFalse(SelectionValidator(prog_code=self.prog_code, stage=self.stage, mod_codes=mod_codes,
                                            entry_year=self.entry_year).validate(),
                         "A selection with too few strand modules is valid.")

        # Selecting the correct number of STRAND modules should return True.
        mod_codes.add(ai2.mod_code)
        self.assertTrue(SelectionValidator(prog_code=self.prog_code, stage=self.stage, mod_codes=mod_codes,
                                           entry_year=self.entry_year).validate(),
                        "A selection with the correct number of strand modules is valid.")

        # Selecting too many STRAND modules with no further OPTS rules to accommodate the extra returns False.
        mod_codes.add(ai3.mod_code)
        self.assertFalse(SelectionValidator(prog_code=self.prog_code, stage=self.stage, mod_codes=mod_codes,
                                            entry_year=self.entry_year).validate(),
                         "A selection with too many strand modules is invalid if extra are not also in OPTS.")

        # Adding an OPTS option rule should now cover the extra STRANDS module.
        OptionRule.objects.create(
            prog_code=self.p1, mod_code_pattern="cs2,iy2", constraint_type="OPTS", stage=1, entry_year='2019',
            min_quantity=1, max_quantity=1
        )
        self.assertTrue(SelectionValidator(prog_code=self.prog_code, stage=self.stage, mod_codes=mod_codes,
                                           entry_year=self.entry_year).validate(),
                        "A selection with too many strand modules is VALID if the remainder is in opts.")

        # Finally, another optional module will go over the OPTS quantity and so should return false.
        extra_opts = Module.objects.create(mod_code="cs2manymodules", title="aint gonna need it")
        mod_codes.add(extra_opts.mod_code)
        self.assertFalse(SelectionValidator(prog_code=self.prog_code, stage=self.stage, mod_codes=mod_codes,
                                            entry_year=self.entry_year).validate())

    def test_simple_opts_selection(self):
        """Tests that a selection of simple OPTS modules is correct, not considering any STRANDS that may overlap."""
        opts1 = Module.objects.create(mod_code="cs21", title="Optional Science")
        opts2 = Module.objects.create(mod_code="cs22", title="Optional Mathematics")
        opts3 = Module.objects.create(mod_code="iy23", title="Optional WhateverYouFeelLikeStudying")
        OptionRule.objects.create(
            prog_code=self.p1, mod_code_pattern="cs2,iy2", constraint_type="OPTS", stage=1, entry_year='2019',
            min_quantity=2, max_quantity=2)
        mod_codes = {opts1.mod_code}
        self.assertFalse(SelectionValidator(prog_code=self.prog_code, stage=self.stage, mod_codes=mod_codes,
                                            entry_year=self.entry_year).validate(),
                         "A selection with too few OPTS modules is valid.")
        mod_codes.add(opts2.mod_code)
        self.assertTrue(SelectionValidator(prog_code=self.prog_code, stage=self.stage, mod_codes=mod_codes,
                                           entry_year=self.entry_year).validate(),
                        "A selection with the correct number of OPTS modules is valid.")
        mod_codes.add(opts3.mod_code)
        self.assertFalse(SelectionValidator(prog_code=self.prog_code, stage=self.stage, mod_codes=mod_codes,
                                            entry_year=self.entry_year).validate(),
                         "A selection with too many OPTS modules is invalid.")
