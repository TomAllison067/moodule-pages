from django.test import TestCase

from modulesApplication.database.csv_reader import CsvReader
from modulesApplication.database.models import Module


class TestCsvReader(TestCase):
    """
    This tests that the csv reader can read in correct headers csv file.
    """
    module_table_headers = ['mod_code', 'jacs_code', 'hecos_code', 'title', 'short_title', 'level', 'department',
                            'with_effect_from', 'availability_terms', 'credits', 'corequisites', 'prerequisites',
                            'banned_combinations', 'learning_outcomes', 'summary', 'notional_learning_hours',
                            'books_to_purchase', 'core_reading', 'exam_format', 'status', 'project', 'lab_hours',
                            'deg_progs']
    strand_table_headers = ['mod_code', 'strand']

    cr = CsvReader()  # The reader
    test_module = Module(  # The first module in the file "exported_sqlite3_module_table.csv"
            mod_code="CS3810",
            jacs_code="",
            hecos_code="",
            title="Half Unit Project",
            short_title="",
            level=6,
            department="Computer Science",
            with_effect_from="",
            availability_terms="",
            credits=15,
            corequisites="",
            prerequisites="CS2800",
            banned_combinations="",
            learning_outcomes="understand complex ideas and identify solutions to a problem, apply scientific and "
                              "software/hardware techniques to solving a problem, analyse the solution to a problem "
                              "and evaluate the associated results, demonstrate the ability to plan, organise and "
                              "present the project work both in written form and orally.",
            summary="To provide the opportunity to demonstrate independence and originality, to plan and organise a "
                    "large project over a long period, and to put into practice the techniques taught throughout "
                    "their degree course.",
            notional_learning_hours=150,
            books_to_purchase="",
            core_reading="Nancy A. Lynch: Distributed Algorithms. The Morgan Kaufmann Series in Data Management "
                         "Systems (1996). ISBN-13: 978-1558603486 "
                         "Hagit Attiya, Jennifer Welch: Distributed Computing: Fundamentals, Simulations and Advanced "
                         "Topics. John Wiley & "
                         "Sons; 2 edition (11 Mar. 2004). ISBN-13: 978-0471453246 "
                         "Christian Cachin, Rachid Guerraoui, Luís Rodrigues: Introduction to Reliable and Secure "
                         "Distributed Programming. Springer 2 edition (11 Feb. 2011).  ASIN: B008R61LBG "
                         "Maurice Herlihy, Nir Shavit: The Art of Multiprocessor Programming. Morgan Kaufmann; "
                         "Revised edition edition (2012). ISBN-13: 978-0123973375",
            exam_format="Time allowed: 2 hours"
                        "Answer ALL questions"
                        "Calculators are NOT permitted",
            status="ACTIVE",
            project=1,
            lab_hours=0,
            deg_progs="CS")

    # How many rows of modules are in "exported_sqlite3_module_table.csv". 114 rows, minus 1 header row = 113.
    MODULES_CSV_ROW_COUNT = 113

    def test_reads_correct_csv_headers(self):
        """
        Test that the reader reads in the correct headers for the Module data model when reading from a csv exported
        from the example sqlite3 database.
        """
        # First try the Module headers
        self.assertEqual(self.module_table_headers,
                         self.cr.read_headers(
                             filename="modulesApplication/tests/resources/exported_sqlite3_module_table.csv"),
                         "The module headers have not been read correctly.")
        # And now the strands headers
        self.assertEqual(self.strand_table_headers,
                         self.cr.read_headers(
                             filename="modulesApplication/tests/resources/exported_strands_table.csv"),
                         "The Strand table headers have not been read correctly.")

    def test_reads_one_module(self):
        """
        Test the reader can successfully read in the first module of the csv file, and return a Module object
        with the correct primary key.
        Note: Django compares equality between model.Model classes on the primary key.
        We could test the rest of the attributes by looking at each instance's __dict__, but there are formatting
        issues between strings in the test_module and the read-in module (eg in newline characters in 'summary') that
        would always return False.
        """
        # The first module in exported_sqlite3_module_table.csv
        modules = self.cr.read_table(
            filename="modulesApplication/tests/resources/exported_sqlite3_module_table.csv",
            model="Module")

        # Django compares quality on primary keys, in this case the module code
        self.assertEqual(self.test_module, modules[0])

    def test_reads_in_correct_number_of_modules(self):
        """
        Tests that the csv reader does indeed read in the correct number of modules from the csv file. The length of the
        list of modules it returns should be 113.
        """
        modules = self.cr.read_table(
            filename="modulesApplication/tests/resources/exported_sqlite3_module_table.csv",
            model="Module")
        self.assertEqual(self.MODULES_CSV_ROW_COUNT, len(modules))

