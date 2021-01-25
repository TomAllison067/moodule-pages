from django.test import TransactionTestCase
from modulesApplication.models import Strands, Module


class MyTestCase(TransactionTestCase):
    def setUp(self):
        m = Module(mod_code="CS2815", title="Small Enterprise Team Project", level=2, department="CS")
        m.save()
        print(Module.objects.first().mod_code)
        Module.objects.e
        self.newstrand = Strands(mod_code=Module.objects.first(), strand='CM')

    def test_empty(self):
        """
        Test to check there are no Strands in the database
        """
        self.assertFalse(Strands.objects.exists())

    
