Medicine Price Registry
=======================

Retail medicine prices are regulated in South Africa through the Single Exit Price Mechanism. These prices are published on a regular basis at http://www.mpr.gov.za. The information is only available in a large and unwieldy excel spreadsheet making it inaccessible to casual users.

This projects builds an API and basic user interface to query this database. You can find a running instance at https://medicineprices.org.za/.

A typical use-case would be for a consumer to look for alternative products for a particular medicine, often generic medicines can be much cheaper than the branded product.
Another use-case allows consumers to ensure that they are not being overcharged for their medicines. This database publishes the maximum price at which a medicine can be sold. A pharmacy cannot legally increase the price of a particular medicine above the price listed here.


Updating the database
---------------------

1. Download the latest public domain NAPPI file from https://www.medikredit.co.za/products-and-services/nappi/nappi-public-domain-file/

       wget https://www.medikredit.co.za/wp-content/mk-data-files/nappi-pub/PUBDOM.zip -P data/nappi_codes
       unzip data/nappi_codes/PUBDOM.zip -d data/nappi_codes/

2. Download the latest SEP file

  a. visit https://www.health.gov.za/nhi-pee/

  b. click on Databases

  c. Download the Database Of Medicine Prices file with the latest date

  d. move it to the `data` directory

3. Run the import

        docker compose run --rm web python manage.py loadsepdata data/LatestSEPDatabase....xlsx

4. Check that the updates look sensible.

5. Commit the changes to mpr.db in git

6. Deploy the changes.


API
---

In addition to providing this simple web interface, we make available a rudimentary API that you can use to access the most up-to-date prices to be used in third party applications.

### Version 2
Basic search e.g.
[https://medicineprices.org.za/api/v2/search-lite?q=lamictin](https://medicineprices.org.za/api/v2/search-lite?q=lamictin)

A more comprehensive search that makes available additional fields
[https://medicineprices.org.za/api/v2/search?q=lamictin](https://medicineprices.org.za/api/v2/search?q=lamictin)

Accessing product details
[https://medicineprices.org.za/api/v2/detail?nappi=703312001](https://medicineprices.org.za/api/v2/detail?nappi=703312001)

Finding generic products (based in active ingredients)
[https://medicineprices.org.za/api/v2/related?nappi=703312001](https://medicineprices.org.za/api/v2/related?nappi=703312001)

Downloading a dump of the entire database
[https://medicineprices.org.za/api/v2/dump](https://medicineprices.org.za/api/v2/dump)

Get the last updated date
[https://medicineprices.org.za/api/v2/last-updated](https://medicineprices.org.za/api/v2/last-updated)

### Version 1
This version of the API used database IDs to lookup medicines. The result was that urls that included the IDs didn't resolve to the same medicines when the database updated.


Basic search e.g.
[https://medicineprices.org.za/api/search-lite?q=lamictin](https://medicineprices.org.za/api/search-lite?q=lamictin)

A more comprehensive search that makes available additional fields
[https://medicineprices.org.za/api/search?q=lamictin](https://medicineprices.org.za/api/search?q=lamictin)

Accessing product details
[https://medicineprices.org.za/api/detail?product=3841](https://medicineprices.org.za/api/detail?product=3841)

Finding generic products (based in active ingredients)
[https://medicineprices.org.za/api/related?product=3841](https://medicineprices.org.za/api/related?product=3841)

Downloading a dump of the entire database
[https://medicineprices.org.za/api/dump](https://medicineprices.org.za/api/dump)


Contributing
------------

To work on this project locally, run

    docker compose up

nodejs and yuglify are apparently needed, but somehow it still works locally?!

On Linux, you probably want to set the environment variables `USER_ID=$(id -u)`
and `GROUP_ID=$(id -g)` where you run docker compose so that the container
shares your UID and GID. This is important for the container to have permission
to modify files owned by your host user (e.g. for python-black) and your host
user to modify files created by the container (e.g. migrations).


Deployment
----------

This app is hosted on dokku or Heroku.

To deploy to an existing dokku (or heroku) server:

1. `git remote add dokku dokku@dokku10.openup.org.za:medicineprices-prod`
2. `git push dokku master`

To deploy to a new heroku instance:

1. `heroku login`
2. `heroku apps:create APP-NAME`
3. `heroku config:set DJANGO_DEBUG=false DJANGO_SECRET_KEY=some-secret-key`
4. `git push heroku`


TODO
----

* Allow for searching of related products
* Create a script that downloads the latest database instead of shipping a sqlite db with the repo
* It might be useful to compare prices over time
* Seems like there are some spelling errors in the database - e.g. paracetamol and paracetemol. Might need to clean the database through some sort of fuzzy match and possibly report those errors back to mpr


Contributors
------------

- Adi Eyal - @soapsudtycoon
- Shaun O'Connell - @ndorfin
