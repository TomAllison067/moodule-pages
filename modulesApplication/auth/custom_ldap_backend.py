import re

from django.contrib.auth.models import Group
from django_auth_ldap.backend import LDAPBackend

from modulesApplication.database.student_profile import StudentProfile


class CustomLDAPBackend(LDAPBackend):
    """
    A custom override of the LDAP backend. The justification is to derive group memberships upon login and then
    add the resulting Django user to the correct Django group (in our case, Students or Staff).

    Only RHUL students and academic or administrative staff should be allowed to log in.

    All other LDAPBackend features work as normal.

    See https://django-auth-ldap.readthedocs.io/en/latest/
    """

    def authenticate_ldap_user(self, ldap_user, password):
        user = ldap_user.authenticate(password)
        if user:
            django_group = self.derive_group(user)
            if not django_group:
                return None  # Don't authenticate if their LDAP group can't match up to one of ours
            user.groups.add(django_group)  # Add the user to the correct group
            if django_group.name == 'Students':
                self.populate_student_profile(user)
        return user

    @staticmethod
    def derive_group(user):
        """
        Given the user attempting to authenticate, this searches the corresponding LDAP attributes to derive if the user
        is staff or a student and returns a Django group.

        It is derived from extensionAttribute8 in the University's LDAP entries for people.

        Values of extensionAttribute8 in LDAP we allow are:
            * Staff (Academic Staff)
            * Staff (Administrative Staff)
            * Student (.....)

        Args:
            user: the user attempting to authenticate

        Returns:
            the correct Group object if the user authenticating is a student, academic staff, or administrative staff. None otherwise.

        """
        ldap_group_value = user.ldap_user.attrs.get('extensionAttribute8')[0].lower()
        if 'academic staff' in ldap_group_value or 'administrative staff' in ldap_group_value:
            group, created = Group.objects.get_or_create(name='Staff')
            return group
        elif 'student' in ldap_group_value:
            group, created = Group.objects.get_or_create(name='Students')
            return group
        else:
            return None

    @staticmethod
    def populate_student_profile(user):
        student_id = user.ldap_user.attrs.get('extensionAttribute3')[0]
        entry_year = user.ldap_user.attrs.get('whenCreated')[0][:4]
        potential_prog_codes = []
        for value in user.ldap_user.attrs.get('memberOf'):
            regex = re.search(r'Programme \d*', value)
            if regex:
                potential_prog_codes.append(regex.group(0))
        if len(potential_prog_codes) != 1:
            prog_code = None
        else:
            prog_code = potential_prog_codes[0].split(' ')[1]
        StudentProfile.populate_student_profile_from_ldap(user=user, student_id=student_id, entry_year=entry_year,
                                                          prog_code=prog_code)
