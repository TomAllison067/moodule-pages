from django.db import IntegrityError
from django.test import TransactionTestCase

from modulesApplication.models import Programme
"""
To use the table we need to import the model required, in this case 'Programmes',
if using foreign keys or querying from multiple table, be sure to import these models.
file location: modulesApplication/models.py
"""


class TestProgrammes(TransactionTestCase):
    """
    writing test to aid our development of the Programmes table

    each testcase must start with 'test' eg test_new_feature or testNewFeature etc.
    """
    def test_one_programme_saved(self):
        Programme.objects.create(prog_code="1067", title="BSc Computer Science", level="BSC")
        self.assertEqual(1, Programme.objects.count(), "One programme saves successfully.")

    def test_no_duplicate_pks(self):
        Programme.objects.create(prog_code="1067", title="BSc Computer Science", level="BSC")
        self.assertRaises(IntegrityError, Programme.objects.create, prog_code="1067", title="Fake", level="BSC")

    def test_two_programmes(self):
        Programme.objects.create(prog_code="1067", title="BSc Computer Science", level="BSC")
        Programme.objects.create(prog_code="1059", title="BSc Computer Science (Artificial Intelligence)", level="BSC")
        self.assertEqual(2, Programme.objects.count(), "Two programmes save successfully.")


"""
As you write and run tests you will need to make changes to the model dependant on how you require the database
(basically TDD)
e.g looking at the Programmes database I might decide to have a composite key of prog_code and title
    then we'd have to edit the 'Meta' of the model to the a unique_together, 
    example of this is in the strands model(modulesApplication/database/models/strand.py)
    
use other models(from /database/models) and tests(from /tests) as a guide to creating tables 

command to run test from specific file: python manage.py test modulesApplication.tests.test_programmes_model
"""