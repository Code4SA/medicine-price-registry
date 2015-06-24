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

Setting up your environment (if you're using virtualenv - which you should be):

    git clone https://github.com/Code4SA/medicine-price-registry.git
    cd medicine-price-registry
    virtualenv $VIRTUALENV_HOME/mpr # (i.e. put it wherever you usually put your virtual environments)
    source $VIRTUALENV_HOME/mpr/bin/active # (or if you're using virtualenvwrapper you can mkvirtualenv mpr; workon mpr)
    pip install -r requirements.txt
    python manage.py runserver

Deployment
==========

This app is hosted on dokku or Heroku.

To deploy to an existing dokku (or heroku) server:

1. `git remote add dokku dokku@dokku.code4sa.org:mpr`
2. `git push dokku`

To deploy to a new heroku instance:

1. `heroku login`
2. `heroku apps:create APP-NAME`
3. `heroku config:set DJANGO_DEBUG=false DJANGO_SECRET_KEY=some-secret-key`
4. `git push heroku`

TODO
====

* Allow for searching of related products
* Create a script that downloads the latest database instead of shipping a sqlite db with the repo
* It might be useful to compare prices over time
* Seems like there are some spelling errors in the database - e.g. paracetamol and paracetemol. Might need to clean the database through some sort of fuzzy match and possibly report those errors back to mpr

Contributors
============
- Adi Eyal - @soapsudtycoon
- Shaun O'Connell - @ndorfin
