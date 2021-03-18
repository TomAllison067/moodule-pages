import getpass

from django.apps import AppConfig
from django.conf import settings


class ModulesApplicationConfig(AppConfig):
    name = 'modulesApplication'

    def ready(self):
        if not settings.TESTING:
            settings.AUTH_LDAP_BIND_DN = input("Please enter LDAP username: ")
            settings.AUTH_LDAP_BIND_PASSWORD = getpass.getpass("Please enter LDAP password: ")
