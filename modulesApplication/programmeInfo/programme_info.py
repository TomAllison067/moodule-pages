from modulesApplication.models import Programme


class ProgrammeInfo:
    def __init__(self, programme: Programme, stages: int, entry_year: str):
        self.__programme = programme
        self.__stages = stages
        self.__entry_year = entry_year

    @property
    def programme(self):
        return self.__programme

    @property
    def stages(self):
        return self.__stages

    @property
    def entry_year(self):
        return self.__entry_year
