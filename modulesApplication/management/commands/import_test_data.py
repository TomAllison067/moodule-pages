import datetime

from django.core.management.base import BaseCommand

from modulesApplication.csv.csv_reader import CsvReader
from modulesApplication.models import *

CURRENT_YEAR = datetime.datetime.now().year


def squash_all():
    """
    TODO - refactor
    squashing all the core modules
    """
    programmes = set(m for m in Programme.objects.all())
    for program in programmes:
        for year in range(2015, CURRENT_YEAR - 1):
            for stage in range(1, 6):
                if OptionRule.objects.filter(prog_code=program,
                                             entry_year=year,
                                             stage=stage).exists():
                    OptionRule.squash_core_modules(program, year, stage)


def clear_database():
    """
    Clear your local database.
    """
    OptionalModule.objects.all().delete()
    OptionRule.objects.all().delete()
    Strands.objects.all().delete()
    Module.objects.all().delete()
    Programme.objects.all().delete()
    People.objects.all().delete()
    CourseLeader.objects.all().delete()
    ModuleVariant.objects.all().delete()


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
        modules = self.cr.read_table_partial("modulesApplication/tests/resources/exported_sqlite3_module_table.csv", Module)
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

    def insert_optional_modules(self):
        """
        Reads the list of optional modules exported from the sqlite3 database view optional_models_by_programme
        into OptionalModule objects.
        """
        cr = CsvReader()
        optional_modules = cr.read_dict(
            'modulesApplication/tests/resources/optional_modules_by_programme.csv')
        for m in optional_modules:
            OptionalModule.objects.create(
                prog_code=Programme.objects.get(prog_code=m['prog_code']),
                mod_code=Module.objects.get(mod_code=m['mod_code']))

    def insert_people(self):
        """Insert all the People into the database."""
        cr = CsvReader()
        people = cr.read_table_partial(
            'modulesApplication/tests/resources/main_people.csv',
            People
        )
        People.objects.bulk_create(people)

    def insert_course_leaders(self):
        cr = CsvReader()
        course_leaders = cr.read_dict(
            'modulesApplication/tests/resources/main_leaders.csv',
        )
        objects = []
        for cl in course_leaders:
            try:
                objects.append(CourseLeader(
                    module=Module.objects.get(mod_code=cl['module']),
                    person=People.objects.get(id=cl['person']),
                    leader=bool(cl['leader']),
                    term=cl['term']
                ))
            except People.DoesNotExist:
                print("Error importing CourseLeader on following row: ")
                print(cl)
                print("Continueing...")
        CourseLeader.objects.bulk_create(objects)

    def insert_module_variants(self):
        cr = CsvReader()
        module_variants = cr.read_dict(
            'modulesApplication/tests/resources/main_module_variants.csv',
        )
        objects = []
        for variant in module_variants:
            try:
                objects.append(ModuleVariant(
                    major=Module.objects.get(mod_code=variant['major']),
                    minor=Module.objects.get(mod_code=variant['minor'])
                ))
            except Module.DoesNotExist:
                print("Unable to find module/s for ModuleVariant on following row:")
                print(variant)
                print("Continueing...")
        ModuleVariant.objects.bulk_create(objects, ignore_conflicts=True)

    def handle(self, *args, **options):
        clear_database()
        self.insert_modules()
        self.insert_strands()
        self.insert_programmes()
        self.insert_optional_modules()
        self.insert_option_rules()
        self.insert_people()
        self.insert_course_leaders()
        self.insert_module_variants()
        squash_all()
        output = "Imported {} modules, {} strands, {} programmes, {} optional modules, {} option rules, {} people, " \
                 "{} course leaders, {} module variants." \
            .format(Module.objects.count(), Strands.objects.count(),
                    Programme.objects.count(), OptionalModule.objects.count(),
                    OptionRule.objects.count(), People.objects.count(), CourseLeader.objects.count(),
                    ModuleVariant.objects.count())
        self.stdout.write(output)
