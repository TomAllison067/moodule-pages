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
        self.__cat_term_in = self.get_cat_term_in()
        self.__modules_dict = modules_dict
        self.__rules_dict = rules_dict
        self.__strand = strand
        self.__has_modules = has_modules

    def get_cat_term_in(self):
        """Complicated way of turning e.g., 2019 into 201920, or 2020 into 202021. Used for rhul course catalogue
        urls, e.g. https://ssb-prod.ec.royalholloway.ac.uk/PROD/bwckctlg.p_disp_catalog_syllabus?cat_term_in=202021
        &subj_code_in=CS&crse_numb_in=1812 """
        return (int(self.__entry_year) * 100) + ((int(
            self.__entry_year) + 1) % 100)

    @property
    def cat_term_in(self):
        return self.__cat_term_in

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
