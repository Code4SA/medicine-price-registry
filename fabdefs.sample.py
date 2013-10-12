from fabric import api

"""
This is a sample fabfile. Customise this fabfile to your settings.
"""

api.env.hosts = ["user@server:port"]
code_dir = "/path/to/code/root"
env_dir = "/path/to/virtualenv/environment"
