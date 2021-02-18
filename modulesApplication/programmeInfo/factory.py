from typing import Dict

from modulesApplication.models import Programme, OptionRule, Module
from .programme_info import ProgrammeInfo


def populate_core_modules(modules_dict: Dict, programme: Programme, stages: int, entry_year: str):
    for stage in range(1, stages + 1):
        stage_key = "stage{}".format(stage)
        rules = OptionRule.objects.filter(prog_code=programme,
                                          entry_year=entry_year,
                                          stage=str(stage),
                                          constraint_type="CORE")
        modules_dict[stage_key]['term1']['CORE'] = []
        modules_dict[stage_key]['term2']['CORE'] = []
        for rule in rules:
            patterns = rule.mod_code_pattern.split(",")
            for pattern in patterns:
                query = Module.objects.filter(mod_code__startswith=pattern)
                for module in query:
                    if module.availability_terms in ["Term 1", "Autumn", "Autumn Term"]:
                        modules_dict[stage_key]['term1']['CORE'] += [module]
                    elif module.availability_terms in ["Term 2", "Spring", "Spring Term"]:
                        modules_dict[stage_key]['term2']['CORE'] += [module]
                    else:
                        modules_dict[stage_key]['term1']['CORE'] += [module]
                        modules_dict[stage_key]['term2']['CORE'] += [module]


def populate_disc_alt_modules(modules_dict, programme, entry_year):
    stage_key = "stage1"
    rules = OptionRule.objects.filter(prog_code=programme,
                                      entry_year=entry_year,
                                      stage='1',
                                      constraint_type="DISC_ALT")
    patterns = [rule.mod_code_pattern for rule in rules]
    modules_dict[stage_key]['term2']['DISC_ALT'] = []
    for pattern in patterns:
        codes = pattern.split(",")
        core_module = Module.objects.get(mod_code=codes[0])
        discretionary_module = Module.objects.get(mod_code=codes[1])
        modules_dict[stage_key]['term2']['CORE'].append(core_module)
        modules_dict[stage_key]['term2']['DISC_ALT'].append([core_module, discretionary_module])


def populate_opts_modules(modules_dict, programme, stages, entry_year):
    for stage in range(2, stages + 1):  # Optional modules start from stage 2
        stage_key = "stage{}".format(stage)
        modules_dict[stage_key]['term1']['OPTS'] = []
        modules_dict[stage_key]['term2']['OPTS'] = []
        rules = OptionRule.objects.filter(prog_code=programme,
                                          entry_year=entry_year,
                                          stage=str(stage),
                                          constraint_type="OPTS")
        optional_modules = [m for m in Module.objects.filter(optionalmodule__prog_code=programme)]
        for rule in rules:
            patterns = rule.mod_code_pattern.split(",")
            for pattern in patterns:
                query = Module.objects.filter(mod_code__startswith=pattern)
                for module in query:
                    if module in optional_modules:
                        if module.availability_terms in ["Term 1", "Autumn", "Autumn Term"]:
                            modules_dict[stage_key]['term1']['OPTS'] += [module]
                        elif module.availability_terms in ["Term 2", "Spring", "Spring Term"]:
                            modules_dict[stage_key]['term2']['OPTS'] += [module]
                        else:
                            modules_dict[stage_key]['term1']['OPTS'] += [module]
                            modules_dict[stage_key]['term2']['OPTS'] += [module]
        #         modules += [module for module in query if module in optional_modules]
        # modules_dict[stage_key]['OPTS'] = modules


def populate_strand_modules(modules_dict, programme, stages, entry_year):
    for stage in range(2, stages + 1):  # strand modules start from stage 2
        stage_key = "stage{}".format(stage)
        modules_dict[stage_key]['term1']['STRAND'] = []
        modules_dict[stage_key]['term2']['STRAND'] = []
        rules = OptionRule.objects.filter(prog_code=programme,
                                          entry_year=entry_year,
                                          stage=str(stage),
                                          constraint_type="STRAND").first()
        if rules:
            strand = rules.mod_code_pattern.split(",")[0]
            patterns = rules.mod_code_pattern.split(",")[1:]
            for pattern in patterns:
                query = Module.objects.filter(strands__strand=strand, mod_code__startswith=pattern)
                for module in query:
                    if module.availability_terms in ["Term 1", "Autumn", "Autumn Term"]:
                        modules_dict[stage_key]['term1']['STRAND'] += [module]
                    elif module.availability_terms in ["Term 2", "Spring", "Spring Term"]:
                        modules_dict[stage_key]['term2']['STRAND'] += [module]
                    else:
                        modules_dict[stage_key]['term1']['STRAND'] += [module]
                        modules_dict[stage_key]['term2']['STRAND'] += [module]


def get_programme_info(prog_code: str, entry_year: str) -> ProgrammeInfo:
    programme = Programme.objects.get(prog_code=prog_code)
    stages = 3
    if programme.yini:
        stages += 1
    if programme.level == "MSCI":
        stages += 1
    terms = 2
    modules_dict = {"stage{}".format(stage):
                    {"term{}".format(term): {} for term in range(1, terms + 1)}
                    for stage in range(1, stages + 1)}
    populate_core_modules(modules_dict, programme, stages, entry_year)
    populate_disc_alt_modules(modules_dict, programme, entry_year)
    populate_opts_modules(modules_dict, programme, stages, entry_year)
    populate_strand_modules(modules_dict, programme, stages, entry_year)
    return ProgrammeInfo(programme, stages, entry_year, modules_dict)
