from modulesApplication.database.csv_reader import CsvReader
from modulesApplication.models import Programme, OptionRule, Module, Strands, OptionalModule
from modulesApplication.management.commands.import_test_data import Command

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


def read_test_modules():
    """
    Insert modules from the sqlite3 csv into your local database.
    """
    c = Command()
    c.insert_modules()


def read_test_strands():
    c = Command()
    c.insert_strands()


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


def read_optional_modules_dict():
    """
    Reads in the list of optional modules exported from the sqlite3 database view optional_modules_by_programme.
    """
    cr = CsvReader()
    optional_modules = cr.read_dict(
        'modulesApplication/tests/resources/optional_modules_by_programme.csv')
    return optional_modules


def read_optional_modules():
    """
    Reads the list of optional modules exported from the sqlite3 database view optional_models_by_programme
    into OptionalModule objects.
    """
    optional_modules = read_optional_modules_dict()
    for m in optional_modules:
        OptionalModule.objects.create(
            prog_code=Programme.objects.get(prog_code=m['prog_code']),
            mod_code=Module.objects.get(mod_code=m['mod_code']))


def all_optional_modules():
    """
    take the dictionary created in from reading optional_modules_by_programmes.csv
    creates a new dictionary, key = prog_code  and value = all optional mod_codes in prog_code
    """
    programme_codes = set(m.pk for m in Programme.objects.all())

    optional_modules = read_optional_modules_dict()
    programme_options = {}
    for programme in programme_codes:
        programme_modules_list = [x["mod_code"] for x in optional_modules if programme in x["prog_code"]]
        programme_options[programme] = programme_modules_list
    return programme_options
