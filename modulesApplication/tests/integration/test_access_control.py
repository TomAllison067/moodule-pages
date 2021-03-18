from django.contrib.auth.models import User, Group
from django.test import TestCase, Client, tag
from django.urls import reverse


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

        self.user.is_staff = True  # Staff permissions required for the next two
        self.user.save()

        response = c.get('/office/landing', follow=True)
        last_url, status_code = response.redirect_chain[-1]
        self.assertTrue(last_url.startswith('/office/landing'))

        response = c.get('/academic/landing', follow=True)
        last_url, status_code = response.redirect_chain[-1]
        self.assertTrue(last_url.startswith('/academic/landing'))

    def test_non_staff_cannot_access_office_views(self):
        """Tests that non-staff users cannot access the office views"""
        c = Client()
        c.login(username='mr.foo', password='top_secret')

        response = c.get(reverse('modulesApplication:office-landing'), follow=True)
        last_url, status_code = response.redirect_chain[-1]
        self.assertTrue(last_url.startswith('/accounts/login'))

        response = c.get(reverse('modulesApplication:csv', kwargs={
            'model_class': 'Programme'
        }), follow=True)
        last_url, status_code = response.redirect_chain[-1]
        self.assertTrue(last_url.startswith('/accounts/login'))

        response = c.get(reverse('modulesApplication:csv-downloads'), follow=True)
        last_url, status_code = response.redirect_chain[-1]
        self.assertTrue(last_url.startswith('/accounts/login'))

        response = c.get(reverse('modulesApplication:selection-requests'), follow=True)
        last_url, status_code = response.redirect_chain[-1]
        self.assertTrue(last_url.startswith('/accounts/login'))

        response = c.get(reverse('modulesApplication:archived-selection-requests'), follow=True)
        last_url, status_code = response.redirect_chain[-1]
        self.assertTrue(last_url.startswith('/accounts/login'))

        response = c.get(reverse('modulesApplication:print-student-selections'), follow=True)
        last_url, status_code = response.redirect_chain[-1]
        self.assertTrue(last_url.startswith('/accounts/login'))

    def test_non_staff_cannot_access_academic_views(self):
        """Tests that non-staff cannot access academic views"""
        c = Client()
        c.login(username='mr.foo', password='top_secret')

        response = c.get(reverse('modulesApplication:academic-landing'), follow=True)
        last_url, status_code = response.redirect_chain[-1]
        self.assertTrue(last_url.startswith('/accounts/login'))

        response = c.get(reverse('modulesApplication:academic-selection-requests'), follow=True)
        last_url, status_code = response.redirect_chain[-1]
        self.assertTrue(last_url.startswith('/accounts/login'))

        # Class-based views seem to return a 403 instead of a redirect.
        response = c.get(reverse('modulesApplication:view-programmes'), follow=True)
        self.assertEqual(403, response.status_code)

        response = c.get(reverse('modulesApplication:update-programmes', kwargs={
            'pk': '1067'
        }), follow=True)
        self.assertEqual(403, response.status_code)

        # Viewing course leaders
        response = c.get(reverse('modulesApplication:view-course-leaders'), follow=True)
        self.assertEqual(403, response.status_code)

        # Updating course leaders
        response = c.get(reverse('modulesApplication:update-course-leader', kwargs={
            'pk': 'not-necessary'
        }), follow=True)
        self.assertEqual(403, response.status_code)

        # Creating course leaders
        response = c.get(reverse('modulesApplication:create-course-leader'), follow=True)
        self.assertEqual(403, response.status_code)

        # Deleting course leaders
        response = c.get(reverse('modulesApplication:delete-course-leader', kwargs={
            'pk': 'not-necessary'
        }), follow=True)
        self.assertEqual(403, response.status_code)
