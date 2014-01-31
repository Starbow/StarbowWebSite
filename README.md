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

