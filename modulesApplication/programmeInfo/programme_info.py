from modulesApplication.models import Programme


class ProgrammeInfo:
    def __init__(self, programme: Programme):
        self.__programme = programme

    @property
    def programme(self):
        return self.__programme

    @programme.setter
    def programme(self, programme):
        self.__programme = programme
