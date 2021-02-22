from typing import Dict

from modulesApplication.models import Programme, OptionRule, Module, CourseLeader, ModuleVariant
from .programme_info import ProgrammeInfo


def get_term(module: Module):
    course_leaders = CourseLeader.objects.filter(module=module)
    if not course_leaders.exists():
        try:
            course_leaders = CourseLeader.objects.filter(module=ModuleVariant.objects.get(minor=module).major)
        except ModuleVariant.DoesNotExist:
            course_leaders = None
    term = course_leaders.first().term if course_leaders else "Unknown"
    return term


def populate_core_modules(modules_dict: Dict, rules_dict: Dict, programme: Programme, stages: int, entry_year: str):
    for stage in range(1, stages + 1):
        stage_key = "stage{}".format(stage)
        rules = OptionRule.objects.filter(prog_code=programme,
                                          entry_year=entry_year,
                                          stage=str(stage),
                                          constraint_type="CORE")
        rules_dict[stage_key]['CORE'] = [rule for rule in rules]
        modules_dict[stage_key]['term1']['CORE'] = []
        modules_dict[stage_key]['term2']['CORE'] = []
        modules_dict[stage_key]['unknown']['CORE'] = []
        for rule in rules:
            patterns = rule.mod_code_pattern.split(",")
            for pattern in patterns:
                query = Module.objects.filter(mod_code__startswith=pattern)
                for module in query:
                    if module.status == "ACTIVE":
                        term = get_term(module)
                        if term == "1":
                            modules_dict[stage_key]['term1']['CORE'] += [module]
                        elif term == "2":
                            modules_dict[stage_key]['term2']['CORE'] += [module]
                        elif term.upper() == "BOTH" or module.title.upper() == "YEAR IN INDUSTRY":
                            modules_dict[stage_key]['term1']['CORE'] += [module]
                            modules_dict[stage_key]['term2']['CORE'] += [module]
                        else:
                            modules_dict[stage_key]['unknown']['CORE'] += [module]


def populate_disc_alt_modules(modules_dict, rules_dict, programme, entry_year):
    stage_key = "stage1"
    rules = OptionRule.objects.filter(prog_code=programme,
                                      entry_year=entry_year,
                                      stage='1',
                                      constraint_type="DISC_ALT")
    rules_dict[stage_key]['DISC_ALT'] = [rule for rule in rules]
    patterns = [rule.mod_code_pattern for rule in rules]
    modules_dict[stage_key]['term2']['DISC_ALT'] = []
    for pattern in patterns:
        codes = pattern.split(",")
        core_module = Module.objects.get(mod_code=codes[0])
        discretionary_module = Module.objects.get(mod_code=codes[1])
        modules_dict[stage_key]['term2']['CORE'].append(core_module)
        modules_dict[stage_key]['term2']['DISC_ALT'].append([core_module, discretionary_module])


def populate_opts_modules(modules_dict, rules_dict, programme, stages, entry_year):
    for stage in range(2, stages + 1):  # Optional modules start from stage 2
        stage_key = "stage{}".format(stage)
        modules_dict[stage_key]['term1']['OPTS'] = []
        modules_dict[stage_key]['term2']['OPTS'] = []
        modules_dict[stage_key]['unknown']['OPTS'] = []
        rules = OptionRule.objects.filter(prog_code=programme,
                                          entry_year=entry_year,
                                          stage=str(stage),
                                          constraint_type="OPTS")
        rules_dict[stage_key]['OPTS'] = [rule for rule in rules]
        optional_modules = [m for m in Module.objects.filter(optionalmodule__prog_code=programme)]
        for rule in rules:
            patterns = rule.mod_code_pattern.split(",")
            for pattern in patterns:
                query = Module.objects.filter(mod_code__startswith=pattern)
                for module in query:
                    if module.status == "ACTIVE" and module in optional_modules \
                            and (module not in modules_dict[stage_key]['term1']['CORE'] or module not in
                                 modules_dict[stage_key]['term2']['CORE']):
                        term = get_term(module)
                        if term == "1":
                            modules_dict[stage_key]['term1']['OPTS'] += [module]
                        elif term == "2":
                            modules_dict[stage_key]['term2']['OPTS'] += [module]
                        elif term.upper() == "BOTH":
                            modules_dict[stage_key]['term1']['OPTS'] += [module]
                            modules_dict[stage_key]['term2']['OPTS'] += [module]
                        else:
                            modules_dict[stage_key]['unknown']['OPTS'] += [module]


def populate_strand_modules(modules_dict, rules_dict, programme, stages, entry_year):
    for stage in range(2, stages + 1):  # strand modules start from stage 2
        stage_key = "stage{}".format(stage)
        modules_dict[stage_key]['term1']['STRAND'] = []
        modules_dict[stage_key]['term2']['STRAND'] = []
        modules_dict[stage_key]['unknown']['STRAND'] = []
        rules = OptionRule.objects.filter(prog_code=programme,
                                          entry_year=entry_year,
                                          stage=str(stage),
                                          constraint_type="STRAND").first()
        rules_dict[stage_key]['STRAND'] = [rules]
        if rules:
            strand = rules.mod_code_pattern.split(",")[0]
            patterns = rules.mod_code_pattern.split(",")[1:]
            for pattern in patterns:
                query = Module.objects.filter(strands__strand=strand, mod_code__startswith=pattern)
                for module in query:
                    if module.status == "ACTIVE" and (
                            module not in modules_dict[stage_key]['term1']['CORE'] or module not in
                            modules_dict[stage_key]['term2']['CORE']):
                        term = get_term(module)
                        if term == "1":
                            modules_dict[stage_key]['term1']['STRAND'] += [module]
                        elif term == "2":
                            modules_dict[stage_key]['term2']['STRAND'] += [module]
                        elif term.upper() == "BOTH":
                            modules_dict[stage_key]['term1']['STRAND'] += [module]
                            modules_dict[stage_key]['term2']['STRAND'] += [module]
                        else:
                            modules_dict[stage_key]['unknown']['STRAND'] += [module]


def get_strand(rules_dict):
    if rules_dict['stage3']['STRAND']:
        strand = rules_dict['stage3']['STRAND'][0].mod_code_pattern.split(',')[0]
    else:
        strand = None
    return strand


def get_programme_info(prog_code: str, entry_year: str) -> ProgrammeInfo:
    programme = Programme.objects.get(prog_code=prog_code)
    stages = 3
    if programme.yini:
        stages += 1
    if programme.level.upper() == "MSCI":
        stages += 1
    terms = 2
    modules_dict = {"stage{}".format(stage):
                        {"term{}".format(term): {} for term in range(1, terms + 1)}
                    for stage in range(1, stages + 1)}
    rules_dict = {"stage{}".format(stage): {} for stage in range(1, stages + 1)}
    for stage in range(1, stages + 1):
        modules_dict["stage{}".format(stage)]['unknown'] = {}
    populate_core_modules(modules_dict, rules_dict, programme, stages, entry_year)
    populate_disc_alt_modules(modules_dict, rules_dict, programme, entry_year)
    populate_opts_modules(modules_dict, rules_dict, programme, stages, entry_year)
    populate_strand_modules(modules_dict, rules_dict, programme, stages, entry_year)
    return ProgrammeInfo(programme, stages, entry_year, modules_dict, rules_dict)
