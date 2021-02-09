"""The expected number of models to be read in by the csv reader and import management command from the example
CSV files. Refactored to here because these numbers were being used in several test cases."""
EXPECTED_PROGRAMMES = 26  # 26 programmes in "programmes.csv"
EXPECTED_STRANDS = 40  # 42 strands minus 2 invalid ones in "exported_strands_table.csv"
EXPECTED_MODULES = 113  # 113 modules in "exported_sqlite3_module_table.csv"
EXPECTED_OPTION_RULES = 805
