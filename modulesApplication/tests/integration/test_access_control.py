from django.contrib.auth.models import User, Group
from django.test import TestCase, Client, tag


@tag('integration')
class TestAccessControl(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='mr.foo', email='bar@example.com', password='top_secret')
        self.student_group = Group.objects.create(name='Students')

    def test_not_logged_in_redirects_to_login(self):
        """
        Tests that a user not logged in is redirected to the login page.
        """
        c = Client()

        response = c.get('/student/landing', follow=True)
        last_url, status_code = response.redirect_chain[-1]
        self.assertTrue(last_url.startswith('/accounts/login/'))

        response = c.get('/office/landing', follow=True)
        last_url, status_code = response.redirect_chain[-1]
        self.assertTrue(last_url.startswith('/accounts/login/'))

        response = c.get('/academic/landing', follow=True)
        last_url, status_code = response.redirect_chain[-1]
        self.assertTrue(last_url.startswith('/accounts/login/'))

    def test_logged_in_does_not_redirect(self):
        """
        Test that a logged in user is NOT redirected!
        """
        c = Client()
        c.login(username='mr.foo', password='top_secret')

        response = c.get('/student/landing', follow=True)
        last_url, status_code = response.redirect_chain[-1]
        self.assertTrue(last_url.startswith('/student/landing'))

        response = c.get('/office/landing', follow=True)
        last_url, status_code = response.redirect_chain[-1]
        self.assertTrue(last_url.startswith('/office/landing'))

        response = c.get('/academic/landing', follow=True)
        last_url, status_code = response.redirect_chain[-1]
        self.assertTrue(last_url.startswith('/academic/landing'))

    def test_student_cannot_access_office_views(self):
        """Tests that a student is redirected to the login page if they try to access the office views."""
        c = Client()
        self.user.groups.add(self.student_group)
        c.login(username='mr.foo', password='top_secret')

        response = c.get('/office/landing', follow=True)
        last_url, status_code = response.redirect_chain[-1]
        self.assertTrue(last_url.startswith('/accounts/login'))
