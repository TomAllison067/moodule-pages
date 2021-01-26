from modulesApplication.database.csv_reader import CsvReader
from modulesApplication.models import Module, Strands

from django.db import IntegrityError

Module.objects.all().delete()
Strands.objects.all().delete()

cr = CsvReader()
modules = cr.read_table("modulesApplication/tests/resources/exported_sqlite3_module_table.csv", Module)
for m in modules:
    m.clean()
Module.objects.bulk_create(modules)


csv_strands = cr.read_table("modulesApplication/tests/resources/exported_strands_table.csv", Strands)
for strand in csv_strands:
    try:
        strand.save()
    except IntegrityError:
        pass
