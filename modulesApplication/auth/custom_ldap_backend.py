from django.contrib.auth.models import Group
from django_auth_ldap.backend import LDAPBackend


class CustomLDAPBackend(LDAPBackend):
    """
    A custom override of the LDAP backend. The justification is to derive group memberships upon login and then
    add the resulting Django user to the correct Django group.

    All other LDAPBackend features work as normal.
    """

    def authenticate_ldap_user(self, ldap_user, password):
        user = ldap_user.authenticate(password)
        if user:
            django_group = self.derive_group(user)
            if not django_group:
                return None
            user.groups.add(django_group)  # Add the user to the correct group
        return user

    @staticmethod
    def derive_group(user):
        """Given the authenticated user, this searches the corresponding LDAP attributes to derive if the user is
        staff or a student and returns a string corresponding to a Django group in our application.

        It is derived from extensionAttribute8 in the University's LDAP entries for people.

        Examples of extensionAttribute8 in LDAP are:
        - Student (Undergraduate)
        - Student (Postgraduate)
        - Staff (Academic Staff)
        :param user the authenticated user object
        :return the correct Django group, or None
        """
        ldap_group_value = user.ldap_user.attrs.get('extensionAttribute8')[0].lower()
        if 'academic staff' in ldap_group_value or 'administrative staff' in ldap_group_value:
            return Group.objects.get(name='Staff')
        elif 'student' in ldap_group_value:
            return Group.objects.get(name='Students')
        else:
            return None


