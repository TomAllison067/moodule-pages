import getpass
import environ

from django.apps import AppConfig
from django.conf import settings

env = environ.env()

class ModulesApplicationConfig(AppConfig):
    name = 'modulesApplication'

    def ready(self):
        if not settings.TESTING:
            settings.AUTH_LDAP_BIND_DN = env('username')
            settings.AUTH_LDAP_BIND_PASSWORD = env('password')
