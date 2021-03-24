from typing import Dict

from modulesApplication.models import Programme


class ProgrammeInfo:
    """A `ProgrammeInfo` object holds information about a degree programme's `Modules` and `OptionRules` for a given
    entry year and stage.

    This information is passed to the front-end when a user wants to choose their modules. From this object, we can
    display all the relevant information in a dynamically-generated module selection form corresponding to the
    student's degree, entry year, and stage.

    The complexity of getting this information is handled by ``programmeInfo.factory``."""

    def __init__(self, programme: Programme, stage: int, entry_year: str, modules_dict: Dict, rules_dict: Dict,
                 strand: str):
        self.__programme = programme
        self.__stage = stage
        self.__entry_year = entry_year
        self.__cat_term_in = self.__get_cat_term_in()
        self.__modules_dict = modules_dict
        self.__rules_dict = rules_dict
        self.__strand = strand

    def __get_cat_term_in(self):
        """Complicated way of turning e.g., 2019 into 201920, or 2020 into 202021.
        Used for rhul course catalogue urls, e.g.
        https://ssb-prod.ec.royalholloway.ac.uk/PROD/bwckctlg.p_disp_catalog_syllabus?cat_term_in=202021&subj_code_in=CS&crse_numb_in=1812"""
        return (int(self.__entry_year) * 100) + ((int(
            self.__entry_year) + 1) % 100)

    @property
    def cat_term_in(self):
        """The term we are looking at e.g., 201920 or 202021. Used for RHUL course catalogue urls."""
        return self.__cat_term_in

    @property
    def programme(self):
        """
        The corresponding degree programme object.
        """
        return self.__programme

    @property
    def stage(self):
        """The stage this `ProgrammeInfo` object is for."""
        return self.__stage

    @property
    def entry_year(self):
        """The corresponding entry year."""
        return self.__entry_year

    @property
    def modules_dict(self):
        """A dictionary of all `Module` objects categorised by term and `OptionRule` constraint type."""
        return self.__modules_dict

    @property
    def rules_dict(self):
        """A dictionary of all relevant `OptionRule` objects."""
        return self.__rules_dict

    @property
    def strand(self):
        """The strand for this degree programme, if relevant."""
        return self.__strand
