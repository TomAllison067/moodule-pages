from modulesApplication.models import OptionRule, Programme

"""
A set of common queries we may wish to make.
"""


def mod_codes_by_constraint(programme: Programme, entry_year: str, stage: str):
    """
    Returns a dict of (constraint_type: mod_codes[]) pairs for a given Programme, entry_year and stage.
    TODO: this is fairly slow. Can we cache the results somehow?
    :param programme: The Programme for which to get the module codes.
    :param entry_year: The entry year of the Programme you wish to query.
    :param stage: The stage of the Programme for which you wish you get the module codes.
    :return: a dict of (constraint_type: mod_codes[]) pairs.
    """
    degree_options = OptionRule.objects.filter(prog_code=programme, entry_year=entry_year, stage=stage)
    mod_codes = {}  # Put the module codes allowed by the rules into a dict
    for option in degree_options:
        mod_codes[option.constraint_type] \
            = mod_codes.get(option.constraint_type, []) + [m.strip() for m in option.mod_code_pattern.split(',')]
    return mod_codes
