from fabdefs import *
from fabric import api
from fabric.operations import local
import os

python = "%s/bin/python" % env_dir
pip = "%s/bin/pip" % env_dir
server_dir = os.path.join(code_dir, "server")

def deploy():
    local("git push origin master")
    with api.cd(code_dir):
        api.run("git pull origin master")
        api.run("%s install -r %s/requirements/production.txt --quiet" % (pip, code_dir))

        with api.cd(server_dir):
            api.run("%s manage.py collectstatic --noinput --settings=settings.production" % python)

        api.sudo("supervisorctl restart mpr")

def update_database(url):
    """
    Update the database remotely. Expects a url to the updated xls file which can usually be foundat http://mpr.gov.za
    e.g.
    fab update_database:'http://mpr.gov.za/Publish/ViewDocument.aspx?DocumentPublicationId\=1488'
    """
    api.run("curl %s > /tmp/meds.xls" % url)
    with api.cd(server_dir):
        api.run("%s manage.py loaddata /tmp/meds.xls --settings=settings.production" % python)
    
