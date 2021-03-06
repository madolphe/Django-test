# Multi-object tracking application

The aim of this project is to develop a django app providing an online laboratory for the flowers team. Two experiments are currently running on the plateform (Attention training task and learning progress self-evaluation).

# Project information

Django and p5.js are used for running the experiment.

To be hosted on : http://flowers-mot.bordeaux.inria.fr/


## Notes

1. Before serving the application, it is important to populate the database with some hand-coded data. This data is stored inside interface_app/fixtures as Django fixture files (JSON). To load the fixtures, run `$python manage.py loaddata <filename>`.

2. The database must conform to the models as defined in `interface_app/models.py`. To make sure this is satisfied, you can hard-reset the database entirely and remove all migration files, including the 0001_initial.py one. Then, using `django-extensions` (included in the `Pipfile` and setup in `settings.py`), run `python manage.py reset_db` to hard-reset the database, . After performing the hard-reset, create a new initial migration and run the server. You will need to repeat the step in the previous note to re-populate the refreshed DB with hand-coded data.

## Requirements

If you want to run this project localy, you will need python > 3.6. Then use pipenv to install required packages:

`pip install pipenv`
`pipenv install`

To deploy when it's the first time you use:
`cd flowers-ol`
`python scripts/deploy.py -r`

When you add new fixtures, be careful if you are using same pks, loadatas won't work!
@TODO : python script to add new fixture (flush a particular table then load datas again)