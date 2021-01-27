from django.core.management.base import BaseCommand, CommandError

from modulesApplication.database.csv_reader import CsvReader
from modulesApplication.models import Module, Strands


def clear_database():
    """
    Clear your local database.
    """
    Strands.objects.all().delete()
    Module.objects.all().delete()


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

    def handle(self, *args, **options):
        clear_database()
        self.insert_modules()
        self.insert_strands()
        output = "Imported {} modules and {} strands successfully.".format(Module.objects.count(), Strands.objects.count())
        self.stdout.write(output)
