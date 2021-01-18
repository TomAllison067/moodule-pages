# The CS2815 Registration App
An application to allow the students, staff and academics of RHUL CompSci better manage
student module choices in line with their chosen degree specification.

# Development / Project Structure
Django's structure might seem at strange at first. 

We have the root directory `modulesProject`,  which in turn has a subdirectory `modulesProject/modulesProject`. This 
subdirectory contains the ever important `settings.py` which has detailed database information and `urls.py` to organise
the URLs in use across the different Django apps in a given Django project.

`modulesApplication` contains our actual application - the stuff we need to work on. A big professional Django project could
be made up of different apps, which is why they get separated out this way. We'll probably only need the one, but
who knows.

`modulesApplication` includes (subject to change as we develop):
* `admin.py` for registering database models with the application.
* `apps.py` - don't think we need to worry about this yet.
* `models.py` - contains our database models built with Django's ORM.
* `tests.py` - All the unit tests. Very likely this will be quickly divided up into several files in a subdir.
* `views.py` - Where all our views go. Again it's likely this could be divided up into several files in a subdir.  

## Working with a PSQL database
Reference this: https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-14-04

Basically, you need to create a postgresql database, and a user that can access the (development-only) database, and
give the user permission to create new databases as the Django test runner will create a temporary 
test database for any unit testing.
1) Log in to psql `sudo -i -u postgres psql` (or however you like)
2) Create a database: `CREATE DATABASE foobase;`
3) Create a user: `CREATE USER someusername WITH PASSWORD somepassword`
4) Django expects some default settings:
   ```sql
   ALTER ROLE myprojectuser SET client_encoding TO 'utf8';
   ALTER ROLE myprojectuser SET default_transaction_isolation TO 'read committed';
   ALTER ROLE myprojectuser SET timezone TO 'UTC';
   ```
5) Give your user privileges on the database: `GRANT ALL PRIVILEGES ON DATABASE foobase TO someusername;`
6) For testing, Django will create a test database each time, so your user needs to be able to create new databases:
    `ALTER USE someusername CREATEDB;`
   
Then, in your local `.env` file:
```
DEBUG=on
SECRET_KEY=this-is-not-a-secret-key
DATABASE_URL=postgresql://someusername:somepassword@localhost:5432/foobase
```
# !!!! Important
Please please please use branches and proper reintegrate / sync merges and proper commit messages!

## Virtual environments
Rather than install all the Python packages globally, it's easier to use virtual environments.

You can keep your virtual environments anywhere - some people have a whole separate folder for all their different venvs
in one place, but I just keep my project's root directory (making sure the `venv/` folder is in `.gitignore`).

Then packages we need (like `Django`) can be frozen in a `requirements.txt` file with `pip3 freeze > requirements.txt` as
we develop, and to install the requirements you can run `pip3 install -r requirements.txt` (where
`requirements.txt` is also just kept in the project root for everyone to access).

Quick how to:
1. Create a new virtual environment `python3 -m venv venv` (or `python3 -m venv yourchosenfoldername`)
2. Activate it with `source venv/bin/activate` (or something very similar on Windows)
3. You'll see `(venv)` before your terminal's prompt string to know you're in the virtual environment
4. Install any packages with `pip3 install -r requirements.txt`
5. As you develop, if there's a new package you can add it with `pip freeze > requirements.txt`, this will
write all the packages in use in `requirements.txt`
6. Now it should all work nicely, but it'll probably still break somehow.

# Useful Links
### Django Documentation
* https://docs.djangoproject.com/en/3.1/ref/ for the general documentation
* https://docs.djangoproject.com/en/3.1/ref/models/querysets/ relating to database queries/ORM/creating new models
* https://discord.com/channels/799604309251194890/799604309952167971/800018104343330866 relating to testing
* https://docs.djangoproject.com/en/3.1/intro/tutorial01/ 8-part tutorial that covers key Django concepts in context.  
### Scrum
* http://www.goodagile.com/scrumprimer/scrumprimer20.pdf the 20-page scrum primer - really worth a read

### Team
* https://trello.com/teamproject2021group34/home The Trello board
