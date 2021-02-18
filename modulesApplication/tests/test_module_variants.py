from django.db import IntegrityError
from django.test import TestCase

from modulesApplication.models import Module, ModuleVariant


class TestModuleVariants(TestCase):
    def setUp(self):
        self.module1 = Module.objects.create(mod_code="1234")

    def test_simple_module_variant(self):
        major = Module.objects.create(mod_code="CS2810")
        minor = Module.objects.create(mod_code="CS2815")
        ModuleVariant.objects.create(major=major, minor=minor)
        self.assertEqual(1, ModuleVariant.objects.count())

    def test_unique_constraint(self):
        major = Module.objects.create(mod_code="CS2810")
        minor = Module.objects.create(mod_code="CS2815")
        ModuleVariant.objects.create(major=major, minor=minor)
        with self.assertRaises(IntegrityError):
            ModuleVariant.objects.create(major=major, minor=minor)
            self.fail("Error not raised.")