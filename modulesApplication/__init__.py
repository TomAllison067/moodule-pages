"""
The main package for our application.

This package contains all the useful subpackages (our team's code), as well as various a few simple modules
that handle various tasks.

Subpackages:
    * `auth`: Contains a subclass of the django-ldap-auth package and some access control functionality.
    * `csv`: Contains functionality relating to csv upload/download, form input, importing test data from csvs, .etc
    * `database`: Where all the models are defined for use by Django's ORM.
    * `programmeInfo`: Functionality to gather information about a student's potential choices related to their degree programme, and validation of their selection.
    * `views`: All of our web views, i.e. all the functionality of the website / how it responds to HTTP requests

Modules:
    * `admin`: Used by Django to register various database models into the auto-generated admin site. We haven't really used this, but the admin site could prove useful for configuring permissions, groups, .etc in the future should you choose to use this application.
    * `apps`: Used by Django to get information about the application and its settings. Contains one overridden method to prompt the host for their LDAP credentials on startup.
    * `models`: Normally where data model classes go. We simply use this to import our models from the database package instead as we have so many.
    * `urls`: Contains the various url patterns for our application. Referenced by modulesProject.urls to actually "include" the urls in the overall project.

Excluded from the documentation are the packages containing all the tests and database migration files.
"""