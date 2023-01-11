# win-together

A backend Django app for the Win Together marketing site CMS.

## setup

-   clone repo
-   `cd` into repo
-   create virtual environment
    -   `python -m venv venv`
-   activate virtual environment
    -   `source venv/bin/activate`
-   install dependencies
    -   `pip install -r requirements.txt`
-   create `.env` with the following info:

    -   `DB_USER` - database username
    -   `DB_PASSWORD` - database password
    -   `SECRET_KEY` - secret key for project

-   start proxy to connect to production DB
    -   `./cloud_sql_proxy -instances "win-together-cms-374413:us-central1:win-together-cms"=tcp:3306`
-   run server locally
    -   `python manage.py runserver`

## deploy

-   `python manage.py collectstatic`
-   `gcloud app deploy`

## view app logs

-   `gcloud app logs tail -s default`
