from typing import Dict

from modulesApplication.models import Programme


class ProgrammeInfo:
    """A ProgrammeInfo object holds information about a degree programme's modules and optionrules for a given
    entry year and stage. The complexity of getting this information is handled by programmeInfo.factory"""

    def __init__(self, programme: Programme, stage: int, entry_year: str, modules_dict: Dict, rules_dict: Dict,
                 strand: str, has_modules: Dict):
        self.__programme = programme
        self.__stage = stage
        self.__entry_year = entry_year
        self.__modules_dict = modules_dict
        self.__rules_dict = rules_dict
        self.__strand = strand
        self.__has_modules = has_modules

    @property
    def has_modules(self):
        return self.__has_modules

    @property
    def programme(self):
        return self.__programme

    @property
    def stage(self):
        return self.__stage

    @property
    def entry_year(self):
        return self.__entry_year

    @property
    def modules_dict(self):
        return self.__modules_dict

    @property
    def rules_dict(self):
        return self.__rules_dict

    @property
    def strand(self):
        return self.__strand
