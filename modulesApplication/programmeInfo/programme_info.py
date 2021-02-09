from typing import Dict

from modulesApplication.models import Programme


class ProgrammeInfo:
    def __init__(self, programme: Programme, stages: int, entry_year: str, modules_dict: Dict):
        self.__programme = programme
        self.__stages = stages
        self.__entry_year = entry_year
        self.__modules_dict = modules_dict

    @property
    def programme(self):
        return self.__programme

    @property
    def stages(self):
        return self.__stages

    @property
    def entry_year(self):
        return self.__entry_year

    def get_modules(self, stage):
        return self.__modules_dict["stage{}".format(stage)]

    @property
    def modules_dict(self):
        return self.__modules_dict
