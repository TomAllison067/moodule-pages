# Moodule - Team 34
Moodule is a comprehensive portal for both computer science students and staff that allows Students to select their 
module choices for their next year, as well as access information about their courses. On the flip side; office staff 
can use this portal to audit and edit information about courses such as course leaders and course content on the fly.

To see the application deployed on Heroku visit https://moodule-rhul.herokuapp.com/
where you can use the following credentials to access the application as a staff member or a student:

* Username: `Staff_Member`, Password: `@Staff12`
* Username: `abcd123`, Password: `@abcd123`

(or, login with your real university username/password e.g. `zhacxx`)

To install and run the app locally on the Django development server (on Ubuntu - other platforms similarly):

1. Navigate to the root folder
2. Install requirements with `pip3 install -r requirements.txt`. You may be prompted about missing C libraries for LDAP modules - you can obtain these easily in your system's package manager.
3. Create a local `.env` file and fill it with the appropriate details. See `.env.example` for details.
4. `python3 manage.py runserver`

Several useful Django management commands may be of help:
1. `python3 manage.py createsuperuser` to create a local superuser stored in the database.
   You can log in using this and it will not be checked against LDAP. You will have access to all areas of the site.
2. `python3 manage.py test` to run the unit and integration tests.
3. `python3 manage.py import_test_data` to populate the database with test data provided earlier in the course.

See https://docs.djangoproject.com/en/3.1/ref/django-admin/

A very very big thank you to the developers over at https://django-auth-ldap.readthedocs.io/en/latest/ for making it easy to hook up to LDAP!