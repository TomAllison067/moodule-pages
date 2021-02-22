from modulesApplication.models import ModuleSelection, OptionRule


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
        return self.validate_core_rules()

    def validate_core_rules(self) -> bool:
        count = 0
        core_rule = self._rules['CORE'][0]
        patterns = set(core_rule.mod_code_pattern.split(","))
        for mod_code in self._modules_selected:
            if mod_code in patterns:
                count += 1
        return core_rule.min_quantity <= count <= core_rule.max_quantity
