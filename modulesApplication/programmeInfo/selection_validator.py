from modulesApplication.models import ModuleSelection


class SelectionValidator:
    """
    A SelectionValidator can be used to validate whether a given ModuleSelection is valid or not.
    """

    def __init__(self, selection: ModuleSelection):
        self._selection = selection

    def validate(self) -> bool:
        """
        Evaluate this validator's ModuleSelection.
        :return: True if the modules selected are valid for the student's degree, entry year and stage.
        False otherwise.
        """
        pass  # TODO: Not yet implemented.
