from modulesApplication.models import Programme


class ProgrammeInfo:
    def __init__(self, programme: Programme, stages: int):
        self.__programme = programme
        self.__stages = stages

    @property
    def programme(self):
        return self.__programme

    @property
    def stages(self):
        return self.__stages
