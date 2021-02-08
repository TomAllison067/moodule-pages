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


def read_optional_modules():
    """
    Reads in the list of optional modules exported from the sqlite3 database view optional_modules_by_programme.
    """
    cr = CsvReader()
    optional_modules = cr.read_dict(
        'modulesApplication/tests/resources/optional_modules_by_programme.csv')
    return optional_modules

def all_optional_modules():
   # programme_codes = set(m.pk for m in Programme.objects.all())
    programme_codes = {'3449', '2676', '2673', '2845', '3015', '1062', '1069', '2446', '2675', '1067', '2686', '2327',
                       '2687', '3014', '3017', '2843', '3047', '1257', '2844', '2846', '1059', '2677', '3424', '2678',
                       '2674', '3016'}
    optional_modules = read_optional_modules()
    programme_options = {}
    for programme in programme_codes:
        programme_modules_list = [x["mod_code"] for x in optional_modules if programme in x["prog_code"]]
        programme_options[programme] = programme_modules_list
    return programme_options