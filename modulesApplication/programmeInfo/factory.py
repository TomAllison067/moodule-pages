from typing import Dict

from modulesApplication.models import Programme, OptionRule, Module
from .programme_info import ProgrammeInfo


def populate_core_modules(modules_dict: Dict, programme: Programme, stages: int, entry_year: str):
    for stage in range(1, stages+1):
        stage_key = "stage{}".format(stage)
        modules_dict[stage_key] = {}
        rules = OptionRule.objects.filter(prog_code=programme,
                                          entry_year=entry_year,
                                          stage=str(stage),
                                          constraint_type="CORE")
        modules = []
        for rule in rules:
            patterns = rule.mod_code_pattern.split(",")
            for pattern in patterns:
                query = Module.objects.filter(mod_code__startswith=pattern)
                modules += [module for module in query]
        modules_dict[stage_key]["CORE"] = modules


def get_programme_info(prog_code: str, entry_year: str) -> ProgrammeInfo:
    programme = Programme.objects.get(prog_code=prog_code)
    stages = 3
    if programme.yini:
        stages += 1
    if programme.level == "MSCI":
        stages += 1
    modules_dict = {}
    populate_core_modules(modules_dict, programme, stages, entry_year)
    return ProgrammeInfo(programme, stages, entry_year, modules_dict)
