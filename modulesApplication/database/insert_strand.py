from modulesApplication.database.csv_reader import CsvReader
from modulesApplication.models import Strands

cr = CsvReader()
csv_strands = cr.read_table("modulesApplication/tests/resources/exported_strands_table.csv", Strands)

for s in csv_strands:
    s.clean()

for stra in csv_strands:
    stra.save()
