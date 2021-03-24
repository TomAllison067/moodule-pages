import operator
from typing import Dict

from modulesApplication.models import Programme, OptionRule, Module, CourseLeader, ModuleVariant
from .programme_info import ProgrammeInfo


def sort_alphanumerically(modules_dict):
    for term in modules_dict.keys():
        for constraint_type, modules_list in modules_dict[term].items():
            if constraint_type != 'DISC_ALT':
                modules_dict[term][constraint_type] = sorted(modules_dict[term][constraint_type],
                                                             key=operator.attrgetter('mod_code'))


def populate_has_modules(modules_dict):
    for term in modules_dict.keys():
        for constraint_type, modules_list in modules_dict[term].items():
            pass


def get_programme_info(prog_code: str, entry_year: str, stage: int) -> ProgrammeInfo:
    """The factory method to build and return a new ProgrammeInfo object. ProgrammeInfo objects hold information
    about a degree programme's modules and optsrules for a given entry year and stage."""
    programme = Programme.objects.get(prog_code=prog_code)
    modules_dict = {'term1': {},
                    'term2': {}}
    rules_dict = {}
    has_modules = {'term1': True,
                   'term2': False}
    populate_core_modules(modules_dict, rules_dict, programme, stage, entry_year)
    populate_disc_alt_modules(modules_dict, rules_dict, programme, stage, entry_year)
    populate_opts_modules(modules_dict, rules_dict, programme, stage, entry_year)
    populate_strand_modules(modules_dict, rules_dict, programme, stage, entry_year)
    strand = get_strand(entry_year, programme, stage)
    modules_to_set(modules_dict)
    sort_alphanumerically(modules_dict)
    populate_has_modules(modules_dict)
    return ProgrammeInfo(programme, stage, entry_year, modules_dict, rules_dict, strand, has_modules)


def modules_to_set(modules_dict):
    for term in modules_dict.keys():
        for constraint_type, modules_list in modules_dict[term].items():
            if constraint_type != 'DISC_ALT':
                modules_dict[term][constraint_type] = set(modules_dict[term][constraint_type])


def get_term(module: Module):
    course_leaders = CourseLeader.objects.filter(module=module)
    if not course_leaders.exists():
        try:
            course_leaders = CourseLeader.objects.filter(module=ModuleVariant.objects.get(minor=module).major)
        except ModuleVariant.DoesNotExist:
            course_leaders = None
    term = course_leaders.first().term if course_leaders else "unknown"
    return term


def populate_core_modules(modules_dict: Dict, rules_dict: Dict, programme: Programme, stage: int, entry_year: str):
    rules = OptionRule.objects.filter(prog_code=programme,
                                      entry_year=entry_year,
                                      stage=str(stage),
                                      constraint_type="CORE")
    rules_dict['CORE'] = [rule for rule in rules] if rules else None
    for rule in rules:
        patterns = rule.mod_code_pattern.split(",")
        for pattern in patterns:
            query = Module.objects.filter(mod_code__startswith=pattern).order_by('mod_code')
            for module in query:
                if module.status == "ACTIVE":
                    term = get_term(module)
                    if term == "1":
                        modules_dict['term1']['CORE'] = modules_dict['term1'].get('CORE', []) + [module]
                    elif term == "2":
                        modules_dict['term2']['CORE'] = modules_dict['term2'].get('CORE', []) + [module]
                    elif term.upper() == "BOTH" or module.title.upper() == "YEAR IN INDUSTRY":
                        modules_dict['term1']['CORE'] = modules_dict['term1'].get('CORE', []) + [module]
                        modules_dict['term2']['CORE'] = modules_dict['term2'].get('CORE', []) + [module]


def populate_disc_alt_modules(modules_dict, rules_dict, programme, stage, entry_year):
    rules = OptionRule.objects.filter(prog_code=programme,
                                      entry_year=entry_year,
                                      stage=stage,
                                      constraint_type="DISC_ALT")
    if rules:
        rules_dict['DISC_ALT'] = [rule for rule in rules]
        patterns = [rule.mod_code_pattern for rule in rules]
        modules_dict['term2']['DISC_ALT'] = []
        for pattern in patterns:
            codes = pattern.split(",")
            core_module = Module.objects.get(mod_code=codes[0])
            discretionary_module = Module.objects.get(mod_code=codes[1])
            modules_dict['term2']['CORE'].append(core_module)
            modules_dict['term2']['DISC_ALT'].append([core_module, discretionary_module])


def populate_opts_modules(modules_dict, rules_dict, programme, stage, entry_year):
    rules = OptionRule.objects.filter(prog_code=programme,
                                      entry_year=entry_year,
                                      stage=str(stage),
                                      constraint_type="OPTS")
    rules_dict['OPTS'] = [rule for rule in rules]
    optional_modules = [m for m in Module.objects.filter(optionalmodule__prog_code=programme).order_by('mod_code')]
    for rule in rules:
        patterns = rule.mod_code_pattern.split(",")
        for pattern in patterns:
            query = Module.objects.filter(mod_code__startswith=pattern)
            for module in query:
                if module.status == "ACTIVE" and module in optional_modules \
                        and not (module in modules_dict['term1'].get('CORE', []) or module in
                                 modules_dict['term2'].get('CORE', [])):
                    term = get_term(module)
                    if term == "1":
                        modules_dict['term1']['OPTS'] = modules_dict['term1'].get('OPTS', []) + [module]
                    elif term == "2":
                        modules_dict['term2']['OPTS'] = modules_dict['term2'].get('OPTS', []) + [module]
                    elif term.upper() == "BOTH":
                        modules_dict['term1']['OPTS'] = modules_dict['term1'].get('OPTS', []) + [module]
                        modules_dict['term2']['OPTS'] = modules_dict['term2'].get('OPTS', []) + [module]


def populate_strand_modules(modules_dict, rules_dict, programme, stage, entry_year):
    rules = OptionRule.objects.filter(prog_code=programme,
                                      entry_year=entry_year,
                                      stage=str(stage),
                                      constraint_type="STRAND").first()
    rules_dict['STRAND'] = [rules] if rules else None
    if rules:
        strand = rules.mod_code_pattern.split(",")[0]
        patterns = rules.mod_code_pattern.split(",")[1:]
        for pattern in patterns:
            query = Module.objects.filter(strands__strand=strand, mod_code__startswith=pattern).order_by('mod_code')
            for module in query:
                if module.status == "ACTIVE" and not (
                        module in modules_dict['term1']['CORE'] or module in
                        modules_dict['term2']['CORE']):
                    term = get_term(module)
                    if term == "1":
                        modules_dict['term1']['STRAND'] = modules_dict['term1'].get('STRAND', []) + [module]
                    elif term == "2":
                        modules_dict['term2']['STRAND'] = modules_dict['term2'].get('STRAND', []) + [module]
                    elif term.upper() == "BOTH":
                        modules_dict['term1']['STRAND'] = modules_dict['term1'].get('STRAND', []) + [module]
                        modules_dict['term2']['STRAND'] = modules_dict['term2'].get('STRAND', []) + [module]


def get_strand(entry_year, programme, stage):
    strand = str()
    if stage >= 2:  # If stage 2 or above, we can get the derive the programme's strand from an OptionRule
        rule = OptionRule.objects.filter(prog_code=programme, constraint_type="STRAND", stage=stage,
                                         entry_year=entry_year).first()
        strand = rule.mod_code_pattern.split(',')[0] if rule is not None else None
    return strand
