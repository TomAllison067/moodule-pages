from modulesApplication.models import Programme
from .programme_info import ProgrammeInfo


def get_programme_info(prog_code):
    programme = Programme.objects.get(prog_code=prog_code)
    return ProgrammeInfo(programme)
