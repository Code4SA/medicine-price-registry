from fabdefs import *
from fabric import api
from fabric.operations import local
import os

python = "%s/bin/python" % env_dir
pip = "%s/bin/pip" % env_dir

def deploy():
    local("git push origin master")
    with api.cd(code_dir):
        api.run("git pull origin master")
        api.run("%s install -r %s/requirements/production.txt --quiet" % (pip, code_dir))

        with api.cd(os.path.join(code_dir, "server")):
            api.run("%s manage.py collectstatic --noinput --settings=settings.production" % python)

        api.sudo("supervisorctl restart mpr")
