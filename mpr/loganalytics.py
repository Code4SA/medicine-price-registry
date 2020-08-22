from django.conf import settings
import base64
import logging
import names
import datetime
import json

logger = logging.getLogger(__name__)

def test_log_analytics(request, response, event, **properties):
    if not hasattr(test_log_analytics, "events"):
        test_log_analytics.events = []
    test_log_analytics.events.append((event, properties))

def log_analytics(request, response, event, **properties):
    pass
    
