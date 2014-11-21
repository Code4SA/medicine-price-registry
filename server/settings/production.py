from os import environ as env
from base import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG
PIPELINE = False
SECRET_KEY = env.get('DJANGO_SECRET_KEY')

LOGGING["loggers"]["mpr"]["level"] = "ERROR"
