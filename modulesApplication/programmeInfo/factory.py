from modulesApplication.models import Programme
from .programme_info import ProgrammeInfo


def get_programme_info(prog_code):
    programme = Programme.objects.get(prog_code=prog_code)
    stages = 3
    if programme.yini:
        stages += 1
    if programme.level == "MSCI":
        stages += 1
    return ProgrammeInfo(programme, stages)
