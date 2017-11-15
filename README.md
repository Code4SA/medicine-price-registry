Medicine Price Registry
=======================

Retail medicine prices are regulated in South Africa through the Single Exit Price Mechanism. These prices are published on a regular basis at http://www.mpr.gov.za. The information is only available in a large and unwieldy excel spreadsheet making it inaccessible to casual users. 

This projects builds an API and basic user interface to query this database. You can find a running instance at http://mpr.code4sa.org.

A typical use-case would be for a consumer to look for alternative products for a particular medicine, often generic medicines can be much cheaper than the branded product.
Another use-case allows consumers to ensure that they are not being overcharged for their medicines. This database publishes the maximum price at which a medicine can be sold. A pharmacy cannot legally increase the price of a particular medicine above the price listed here.

API
===
In addition to providing this simple web interface, we make available a rudimentary API that you can use to access the most up-to-date prices to be used in third party applications.

### Version 2
Basic search e.g.
[https://mpr.code4sa.org/api/v2/search-lite?q=lamictin](https://mpr.code4sa.org/api/v2/search-lite?q=lamictin)

A more comprehensive search that makes available additional fields
[https://mpr.code4sa.org/api/v2/search?q=lamictin](https://mpr.code4sa.org/api/v2/search?q=lamictin)

Accessing product details
[https://mpr.code4sa.org/api/v2/detail?nappi=703312001](https://mpr.code4sa.org/api/v2/detail?nappi=703312001)

Finding generic products (based in active ingredients)
[https://mpr.code4sa.org/api/v2/related?nappi=703312001](https://mpr.code4sa.org/api/v2/related?nappi=703312001)

Downloading a dump of the entire database
[https://mpr.code4sa.org/api/v2/dump](https://mpr.code4sa.org/api/v2/dump)

Get the last updated date
[https://mpr.code4sa.org/api/v2/last-updated](https://mpr.code4sa.org/api/v2/last-updated)

### Version 1
This version of the API used database IDs to lookup medicines. The result was that urls that included the IDs didn't resolve to the same medicines when the database updated.


Basic search e.g.
[https://mpr.code4sa.org/api/search-lite?q=lamictin](https://mpr.code4sa.org/api/search-lite?q=lamictin)

A more comprehensive search that makes available additional fields
[https://mpr.code4sa.org/api/search?q=lamictin](https://mpr.code4sa.org/api/search?q=lamictin)

Accessing product details
[https://mpr.code4sa.org/api/detail?product=3841](https://mpr.code4sa.org/api/detail?product=3841)

Finding generic products (based in active ingredients)
[https://mpr.code4sa.org/api/related?product=3841](https://mpr.code4sa.org/api/related?product=3841)

Downloading a dump of the entire database
[https://mpr.code4sa.org/api/dump](https://mpr.code4sa.org/api/dump)


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
