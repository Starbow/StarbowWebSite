StarbowWebSite
==============

The app behind starbow.com


Installation
------------

Copy `starbowmodweb/example.config.py` to `starbowmodweb/config.py` and follow configuration:

    cp starbowmodweb/example.config.py starbowmodweb/config.py

First, create the SQL database, `starbow_website`:

    mysql -u root
    ...
    mysql> CREATE DATABASE starbow_website;

Run::

    pip install -r requirements.txt
    python manage.py syncdb
    python manage.py runserver

