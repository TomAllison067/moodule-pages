from django.core.management.base import BaseCommand, CommandError

from modulesApplication.database.csv_reader import CsvReader
from modulesApplication.models import Module, Strands, Programme, OptionRule
import datetime

CURRENT_YEAR = datetime.datetime.now().year


def squash_all():
    """
    TODO - refactor
    squashing all the core modules
    """
    programmes = set(m for m in Programme.objects.all())
    for program in programmes:
        for year in range(2015, CURRENT_YEAR-1):
            for stage in range(1, 6):
                if OptionRule.objects.filter(prog_code=program,
                                             entry_year=year,
                                             stage=stage).exists():
                    OptionRule.squash_core_modules(program, year, stage)


def clear_database():
    """
    Clear your local database.
    """
    OptionRule.objects.all().delete()
    Strands.objects.all().delete()
    Module.objects.all().delete()
    Programme.objects.all().delete()


def all_optional_modules():
    """
    take the dictionary created in from reading optional_modules_by_programmes.csv
    creates a new dictionary, key = prog_code  and value = all optional mod_codes in prog_code
    """
    programme_codes = set(m.pk for m in Programme.objects.all())

    cr = CsvReader()
    optional_modules = cr.read_dict('modulesApplication/tests/resources/optional_modules_by_programme.csv')
    programme_options = {}
    for programme in programme_codes:
        programme_modules_list = [x["mod_code"] for x in optional_modules if programme in x["prog_code"]]
        programme_options[programme] = programme_modules_list
    return programme_options


class Command(BaseCommand):
    """
    A custom Django management command to import the test/development data into your local database.
    """
    help = 'Import the test data into your local database'
    cr = CsvReader()

    def insert_modules(self):
        """
        Insert modules from the sqlite3 csv into your local database.
        """
        modules = self.cr.read_table("modulesApplication/tests/resources/exported_sqlite3_module_table.csv", Module)
        for m in modules:
            m.clean()  # Validate every model's attributes
        Module.objects.bulk_create(modules)  # Create & save to database

    def insert_strands(self):
        """
        Insert Strands from the sqlite3 csv into your local database.
        """
        module_codes = set(m.pk for m in Module.objects.all())
        csv_strands = self.cr.read_table("modulesApplication/tests/resources/exported_strands_table.csv", Strands)
        for strand in csv_strands:
            if strand.module_id not in module_codes:
                csv_strands.remove(strand)
        Strands.objects.bulk_create(csv_strands)

    def insert_programmes(self):
        programmes = self.cr.read_table_partial(
            filepath="modulesApplication/tests/resources/programmes.csv",
            model_class=Programme
        )
        Programme.objects.bulk_create(programmes)

    def insert_option_rules(self):
        rules = self.cr.read_table_partial(
            filepath="modulesApplication/tests/resources/option_rules.csv",
            model_class=OptionRule
        )
        OptionRule.objects.bulk_create(rules)

    def handle(self, *args, **options):
        clear_database()
        self.insert_modules()
        self.insert_strands()
        self.insert_programmes()
        self.insert_option_rules()
        squash_all()
        programme_opt_modules = all_optional_modules()
        OptionRule.squash_all_opts_modules_alt(programme_opt_modules)
        output = "Imported {} modules, {} strands, {} degree programmes and {} option_rules successfully." \
            .format(Module.objects.count(), Strands.objects.count(), Programme.objects.count(),
                    OptionRule.objects.count())
        self.stdout.write(output)
