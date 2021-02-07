from modulesApplication.database.csv_reader import CsvReader
from modulesApplication.models import Programme, OptionRule

"""
A set of utility functions to be used in unit tests.
"""

def read_test_programmes():
    """
    Reads in the test programmes and saves them to the test database.
    """
    Programme.objects.all().delete()
    cr = CsvReader()
    # Read in the programmes
    programmes = cr.read_table_partial(
        filepath="modulesApplication/tests/resources/programmes.csv",
        model_class=Programme
    )
    Programme.objects.bulk_create(programmes)


def read_test_optionrules():
    """
    Reads in the test option rules and saves them to the test database.
    """
    OptionRule.objects.all().delete()
    cr = CsvReader()
    rules = cr.read_table_partial(
        filepath="modulesApplication/tests/resources/option_rules.csv",
        model_class=OptionRule
    )
    OptionRule.objects.bulk_create(rules)
