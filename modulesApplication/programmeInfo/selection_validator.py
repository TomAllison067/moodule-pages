from modulesApplication.models import ModuleSelection, OptionRule, Strands


class SelectionValidator:
    """
    A SelectionValidator can be used to validate whether a given ModuleSelection is valid or not.
    """

    def __init__(self, selection: ModuleSelection):
        self._selection = selection
        self._rules = self.get_rules()
        self._modules_selected = set([m.mod_code for m in self._selection.module_set.all()])

    def get_rules(self):
        query = OptionRule.objects.filter(
            prog_code=self._selection.programme,
            stage=self._selection.stage,
            entry_year=self._selection.entry_year,
        )
        rules = {}
        for rule in query:
            rules[rule.constraint_type] = rules.get(rule.constraint_type, [])
            rules[rule.constraint_type].append(rule)
        return rules

    def validate(self) -> bool:
        """
        Evaluate this validator's ModuleSelection.
        :return: True if the modules selected are valid for the student's degree, entry year and stage.
        False otherwise.
        """
        return self.validate_core_rules() and self.validate_disc_alt_rules() and self.validate_strand_rules()

    def validate_core_rules(self) -> bool:
        """Validates the modules selected against the CORE OptionRules."""
        core_rule = self._rules.get('CORE')[0] if self._rules.get('CORE') else None

        # If there are any core rules, count the modules selected that match the pattern and check that it is correct.
        if core_rule:
            count = 0
            core_rule = self._rules['CORE'][0]
            patterns = set(core_rule.mod_code_pattern.split(","))
            for mod_code in self._modules_selected:
                if mod_code in patterns:
                    count += 1
            return core_rule.min_quantity <= count <= core_rule.max_quantity
        return True

    def validate_disc_alt_rules(self) -> bool:
        """Validates the discretionary alternative OptionRules."""
        rules = self._rules.get('DISC_ALT')

        # Only check if any such rules exist.
        if rules:
            for rule in rules:
                patterns = rule.mod_code_pattern.split(",")
                core = patterns[0]
                alt = patterns[1]
                if core in self._modules_selected and alt in self._modules_selected:
                    return False  # If both are selected, this is invalid.
                elif not (core in self._modules_selected or alt in self._modules_selected):
                    return False  # If neither are selected, this is invalid.
        return True  # If there are no DISC_ALT rules, then this check passes by default.

    def validate_strand_rules(self):
        """Validate the strand OptionRules."""
        rules = self._rules.get('STRAND')
        if rules:
            for rule in rules:
                count = 0
                patterns = rule.mod_code_pattern.split(",")
                strand = patterns[0]
                mod_code_patterns = tuple(set(patterns[1:]))
                for mod_code in self._modules_selected:
                    if mod_code.startswith(mod_code_patterns) and Strands.objects.get(module=mod_code, strand=strand):
                        count += 1
                if not rule.min_quantity <= count <= rule.max_quantity:
                    return False
        return True
