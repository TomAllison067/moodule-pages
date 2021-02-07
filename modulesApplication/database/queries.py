from typing import Dict

from modulesApplication.models import OptionRule, Programme, Module

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
    programme = Programme.objects.get(prog_code=prog_code)
    stages = 3
    if programme.level == "MSC":
        stages += 1
    if programme.yini:
        stages += 1
    patterns = {}
    for i in range(1, stages + 1):
        patterns["stage{}".format(i)] = modcode_patterns_by_constraint(
            programme=programme, entry_year=entry_year, stage='{}'.format(i)
        )
    modules = {stage: {} for stage in patterns.keys()}
    for stage, constraints in patterns.items():
        for constraint, codes in constraints.items():
            modules[stage][constraint] = [Module.objects.get(mod_code=mc) for mc in codes]
    programme_info = {
        'programme': programme,
        'modules': modules,
        'entry_year': entry_year
    }
    return programme_info
