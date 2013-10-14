Medicine Price Registry
=======================

Retail medicine prices are regulated in South Africa through the Single Exit Price Mechanism. These prices are published on a regular basis at http://www.mpr.gov.za. The information is only available in a large and unwieldy excel spreadsheet making it inaccessible to casual users. 

This projects builds an API and basic user interface to query this database. You can find a running instance at http://mpr.code4sa.org.

A typical use-case would be for a consumer to look for alternative products for a particular medicine, often generic medicines can be much cheaper than the branded product.
Another use-case allows consumers to ensure that they are not being overcharged for their medicines. This database publishes the maximum price at which a medicine can be sold. A pharmacy cannot legally increase the price of a particular medicine above the price listed here.

Contributing
============

To work on this project locally, you'll need the following:
- Python
- yuglify (sudo npm install -g yuglify)
- virtualenv (optional)

Setting up your environment (if you're using virtualenv - which you should be)
    git clone https://github.com/Code4SA/medicine-price-registry.git
    cd medicine-price-registry
    virtualenv $VIRTUALENV_HOME/mpr # (i.e. put it wherever you usually put your virtual environments)
    source $VIRTUALENV_HOME/mpr/bin/active # (or if you're using virtualenvwrapper you can mkvirtualenv mpr; workon mpr)
    pip install -r deploy/development.txt
    cd server

    python manage.py runserver --settings=settings.development

Deployment
==========

I've written a basic deployment script to my production server using $PROJECT_ROOT/fabfile.py.

I run the code using gunicorn and supervisord with nginx working as a reverse proxy. The fabfile assumes that the application is called mpr and is run using supervisord. If you're setting it up in the same way, you need to copy fabdefs.sample.py to fabdefs.py and change the relevant settings inside that file. 

At some point I'll add the nginx and supervisord config files to the repo in case anyone cares (and I guess it's probably good practice too).

TODO
====

* Allow for searching of related products
* Create a script that downloads the latest database instead of shipping a sqlite db with the repo
* It might be useful to compare prices over time
* Add CSS pre-compilers
* Seems like there are some spelling errors in the database - e.g. paracetamol and paracetemol. Might need to clean the database through some sort of fuzzy match and possibly report those errors back to mpr

Contributors
============
- Adi Eyal - @soapsudtycoon
- Shaun O'Connell - @ndorfin
