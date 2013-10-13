Medicine Price Registry
=======================

Retail medicine prices are regulated in South Africa through the Single Exit Price Mechanism. These prices are published on a regular basis at http://www.mpr.gov.za. The information is only available in a large and unwieldy excel spreadsheet making it inaccessible to casual users. 

This projects builds and api and basic user interface to query this database. You can find a running instance at http://mpr.code4sa.org.

A typical use-case would be for a consumer to look for alternative products for a particular medicine, often generic medicines can be much cheaper than the branded product.
Another use-case allows consumers to ensure that they are not being overcharged for their medicines. This database publishes the maximum price at which a medicine can be sold. A pharmacy cannot legally increase the price of a particular medicine above the price listed here.

Running the damn thing
======================

If you want to run the code locally.

assuming $PROJECT_ROOT is where you've clone the repo

    cd $PROJECT_ROOT/server
    python manage.py runserver --settings=settings.development

Deployment
==========

I've written a basic deployment script to my production server using $PROJECT_ROOT/fabfile.py.

I run the code using gunicorn and supervisord with nginx working as a reverse proxy. The fabfile assumes that the application is called mpr and is run using supervisord. If you're setting it up in the same way, you need to copy fabdefs.sample.py to fabdefs.py and change the relevant settings inside that file. 

At some point I'll add the nginx and supervisord config files to the repo in case anyone cares (and I guess it's probably good practice too).

TODO
====

* One really important feature that's missing is the ability to search by brand name. It would be cool to be able to search for the brand that you generally buy, then ask for all the similar products for that specific medicine. 
* Create a script that downloads the latest database instead of shipping a sqlite db with the repo
* It might be useful to compare prices over time
