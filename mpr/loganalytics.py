from django.conf import settings
import base64
import logging
import names
import datetime
import amplitude
import json

logger = logging.getLogger(__name__)
amplitude_logger = amplitude.AmplitudeLogger(api_key=settings.AMPLITUDE_KEY)

def test_log_analytics(request, response, event, **properties):
    if not hasattr(test_log_analytics, "events"):
        test_log_analytics.events = []
    test_log_analytics.events.append((event, properties))

def log_analytics(request, response, event, **properties):
    ids = [(k, v) for (k, v) in request.COOKIES.items() if "amplitude_id_" in k]
    try:
        if len(ids) > 0:
            amp_id = ids[0][1]
            decoded = base64.b64decode(ids[0][1])
            js = json.loads(decoded)
            user_id = js["userId"]
            device_id = js["deviceId"]
        else:
            device_id = None
            user_id = "Anonymous"

        event_args = {
            "event_type": event,
            "user_id" : js["userId"], "device_id" : js["deviceId"],
            "source":"test",
            "event_properties" : properties
        }
        event = amplitude_logger.create_event(**event_args)
        amplitude_logger.log_event(event)
    except Exception as e:
        logger.exception("Error handling analytics")
