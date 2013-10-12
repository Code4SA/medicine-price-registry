from fabdefs import *
from fabric import api
import os

python = "%s/bin/python" % env_dir
pip = "%s/bin/pip" % env_dir

def deploy():
    with api.cd(code_dir):
        api.run("git pull origin master")
        api.run("%s install -r %s/deploy/production.txt --quiet" % (pip, code_dir))

        with api.cd(os.path.join(code_dir, "server")):
            api.run("%s manage.py collectstatic --noinput" % python)

        api.sudo("supervisorctl restart mpr")
