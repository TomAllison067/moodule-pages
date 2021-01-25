from modulesApplication.database.csv_reader import CsvReader
from modulesApplication.models import Module

cr = CsvReader()
modules = cr.read_table("modulesApplication/tests/resources/exported_sqlite3_module_table.csv",
                        Module)
for m in modules:
    m.clean()

Module.objects.bulk_create(modules)
