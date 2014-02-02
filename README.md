# StarbowWebSite


The app behind starbow.com


## Installation

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

## SASS

Our CSS code is compiled using [SASS](http://sass-lang.com/), Syntactically Awesome Style Sheets. To compile the SASS code into CSS, you must first install the SASS compiler.

First, [install ruby](https://www.ruby-lang.org/en/downloads/) if you do not have it installed.

To install sass, just run:

    gem install sass

The best way to work with SASS is to have it watch the `*.scss` files for changes and compile new CSS as the SCSS code is changed. To begin doing so, navigate to the `scss` directory (`starbowmodweb/site/static/site/css/scss`), and run the following:

    sass --watch app.scss:../app.css --style compressed

This will automatically compile `app.css` any time you change any `*.scss` file in that directory.

## Deploying

Before deploying you need to copy all static files to the static directory using:

    python manage.py collectstatic


### Using Apache2

    Alias /forum/ /path/to/forum/root/
    Alias /wiki/ /path/to/wiki/root/
    Alias /media/ /path/to/media/directory/
    Alias /static/ /path/to/static/directory/

    <Directory /path/to/media/directory/>
    Order deny,allow
    Require all granted
    </Directory>

    <Directory /path/to/static/directory/>
    Order deny,allow
    Require all granted
    </Directory>

    WSGIScriptAlias / /path/to/StarbowWebSite/starbowmodweb/apache/wsgi.py
    WSGIPythonPath /path/to/StarbowWebSite/

    <Directory /path/to/StarbowWebSite/starbowmodweb/apache>
    <Files wsgi.py>
    Order deny,allow
    Require all granted
    </Files>
    </Directory>
