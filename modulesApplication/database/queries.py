from typing import Dict

from modulesApplication.models import OptionRule, Programme, Module, Strands

"""
A set of common queries we may wish to make.
"""


def modcode_patterns_by_constraint(programme: Programme, entry_year: str, stage: str) -> Dict[str, list]:
    """
    Returns a dict of (constraint_type: mod_codes_patterns[]) pairs for a given Programme, entry_year and stage.

    TODO: this is fairly slow. Can we cache the results somehow?

    :param programme: The Programme for which to get the module codes.
    :param entry_year: The entry year of the Programme you wish to query.
    :param stage: The stage of the Programme for which you wish you get the module codes.
    :return: a dict of (constraint_type: mod_code_patterns[]) pairs.
    """
    degree_options = OptionRule.objects.filter(prog_code=programme, entry_year=entry_year, stage=stage)
    mod_codes = {}  # Put the module codes allowed by the rules into a dict
    for option in degree_options:
        mod_codes[option.constraint_type] \
            = mod_codes.get(option.constraint_type, []) + [m.strip() for m in option.mod_code_pattern.split(',')]
    return mod_codes


def get_programme_info(prog_code: str, entry_year):
    """
    TODO the output is just BEGGING to be made into a proper class, not just some haphazard dict!
    TODO REFACTOR THIS IS TERRIBLE - Put the main keys as programme, year, stage. Process each rule individually.
    TODO just everything tbh

    Given a programme code and an entry year, returns a Dict object containing information about that Programme's
    modules and constraints.

    An example output:
    info['programme'] - the corresponding Programme object
    info['entry_year'] - a String of the entry year
    info['modules'] - A mapping of stages to constraint types to a list of Module objects, for example:
        {'stage1': {'DISC_ALT': [<Module: Module object (CS1812)>, <Module: Module object (CS1813)>, ....
    info['rules'] - A mapping of stages to OptionRule objects, for example:
        {'stage1': [<OptionRule: OptionRule object (14539)>, <OptionRule: OptionRule object (14540)>, ....


    :param prog_code: A string of the programme code to query
    :param entry_year: A string of the entry year
    :return: A dictionary containing programme info
    """
    programme = Programme.objects.get(prog_code=prog_code)  # The Programme object we are analysing
    stages = 3  # All degrees have 3 stages to begin with.
    if programme.level.upper() == "MSCI":
        stages += 1
    if programme.yini:
        stages += 1
    info = {  # This will get sent to the template.
        'programme': programme,
        'entry_year': entry_year,
        'modules': {},  # A list of module objects (used to display on the frontend)
        'rules': {}  # A list of OptionRule objects (used for validation)
    }
    print("STAGES ", stages)
    # Populate the dict with the rules and modules from stage 1 until the last stage
    for stage in range(1, stages + 1):
        stage_key = 'stage{}'.format(stage)

        # All the OptionRules for this stage
        rules = OptionRule.objects.filter(prog_code=programme,
                                          entry_year=entry_year,
                                          stage=str(stage))
        info['rules'][stage_key] = [rule for rule in rules]

        # Next, populate the modules
        info['modules'][stage_key] = {}

        # TODO ask the waiter to take this spaghetti back
        # For each OptionRule, split the mod_code_patterns and query a list of Module objects applicable for this degree
        for rule in rules:
            if rule.constraint_type in ["CORE", "OPTS", "DISC_ALT", "STRAND", "CREDITS"]:
                modules = []
                patterns = rule.mod_code_pattern.split(",")
                for pattern in patterns:
                    if rule.constraint_type == "STRAND":
                        strand = patterns[0]
                        query = Module.objects.filter(mod_code__startswith=pattern, strands__strand=strand)
                    else:
                        query = Module.objects.filter(mod_code__startswith=pattern)
                    for module in query:
                        modules.append(module)
                info['modules'][stage_key][rule.constraint_type] = \
                    info['modules'][stage_key].get(rule.constraint_type, []) + modules
        print(info['rules'])
    return info
