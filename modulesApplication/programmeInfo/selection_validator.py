from modulesApplication.models import ModuleSelection, OptionRule, Strands


class SelectionValidator:
    """
    A SelectionValidator can be used to validate whether a given ModuleSelection is valid or not.

    Validation is (attempted) performed as such:

    1. First, it checks that the correct number of CORE modules are selected. It assumes there is one CORE OptionRule,
    which has all the mod_code_patterns for the CORE modules and the correct min/max quantity (min and max are
    probably the same number).

    2. Next, it checks the DISC_ALT rules. DISC_ALT OptionRules specify two modules, one as the default and one
    as the discretionary alternative. It checks that one OR the other is selected. The selection is invalid if
    both or neither modules are selected.

    3. Next, it checks the STRAND rules. A selection is invalid if not enough STRAND modules are selected. If
    too many are selected, the 'extra' STRAND modules are not checked against STRAND rules. Instead, they are
    'carried over' into the OPTS check. For example, somebody on the AI course must select exactly two AI modules
    in third year, but still has optional modules to select (some of which may happen to be AI modules as well),
    and although this is over the quantity specified by the STRAND OptionRule it is still a valid selection.

    4. Finally, it checks the OPTS rules. Any remaining modules are optional choices, and some of these optional
    choices may be carried-over STRAND modules. If not enough or too many such modules are selected, the selection
    is invalid.

    As modules are "validated", they are added to a set and removed from the initial selected set. As a safety-net,
    a selection is invalid if there are any modules remaining in this initial set (because the user may have selected
    too many, or the module might be a 'rogue' module, or some other unforeseen bug - either way, any remaining
    modules are invalid).
    """

    def __init__(self, selection: ModuleSelection):
        self._selection = selection
        self._rules = self.get_rules()
        self._modules_selected = set([m.mod_code for m in self._selection.module_set.all()])
        self._confirmed = set()

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
        print(rules['OPTS'])
        return rules

    def validate(self) -> bool:
        """
        Evaluate this validator's ModuleSelection.
        :return: True if the modules selected are valid for the student's degree, entry year and stage.
        False otherwise.
        """
        valid = self.validate_core_rules() and self.validate_disc_alt_rules() and self.validate_strand_rules() and \
                self.validate_opts_rules() and len(self._modules_selected) == 0
        return valid

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
                    self._confirmed.add(mod_code)
            self._modules_selected = self._modules_selected.difference(self._confirmed)
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
                elif core in self._modules_selected:
                    self._confirmed.add(core)
                elif alt in self._modules_selected:
                    self._confirmed.add(alt)
                else:
                    return False  # If neither are in, this is invalid.
                self._modules_selected = self._modules_selected.difference(self._confirmed)
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
                    if mod_code.startswith(mod_code_patterns) \
                            and Strands.objects.filter(module__mod_code__startswith=mod_code, strand=strand) \
                            and count + 1 <= rule.max_quantity:  # Any overlaps will be checked by OPTS.
                        count += 1
                        self._confirmed.add(mod_code)
                if not rule.min_quantity <= count <= rule.max_quantity:
                    print("Failed on strand")
                    return False
                self._modules_selected = self._modules_selected.difference(self._confirmed)
        return True

    def validate_opts_rules(self):
        """Validate the OPTS rules."""
        rules = self._rules.get('OPTS')
        if rules:
            for rule in rules:
                count = 0
                mod_code_patterns = tuple(set(rule.mod_code_pattern.split(",")))
                for mod_code in self._modules_selected:
                    if count == rule.max_quantity:
                        # Handles degrees with multiple opts rules with different quantities
                        break
                    if mod_code.startswith(mod_code_patterns):
                        count += 1
                        self._confirmed.add(mod_code)
                if not rule.min_quantity <= count <= rule.max_quantity:
                    print("Failed on opts", rule, rule.min_quantity, rule.max_quantity)
                    return False
                self._modules_selected = self._modules_selected.difference(self._confirmed)
        return True
