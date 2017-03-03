from django.conf import settings
import logging
import names
import datetime

logger = logging.getLogger(__name__)

def log_analytics(request, response, event, properties):
    try:
        import analytics
        from ipware.ip import get_ip as get_ip

        if settings.DEBUG: return
        if not hasattr(settings, "SEGMENT_IO_KEY"):
            logger.warning("Cannot send analytics. No Segment IO Key has been set")
            return

        if "pingdom" in request.META.get("HTTP_USER_AGENT", ""):
            logger.warning("Not recording analytics. Ignored pingdom bot")
            return

        api_key = settings.SEGMENT_IO_KEY

        ip = get_ip(request)

        uid = names.get_full_name()
        uid = request.COOKIES.get("uid", uid)
        set_cookie(response, "uid", uid)

        request.session["uid"] = uid
        analytics.init(api_key)
        analytics.identify(uid, {
                "$name" : uid,
            },
            { "$ip" : ip}
        )
        analytics.track(uid, event=event, properties=properties)
    except Exception, e:
        logger.exception("Error handling analytics")


def set_cookie(response, key, value, days_expire = 7):
    max_age = 365 * 24 * 60 * 60  * 100
    expires = datetime.datetime.strftime(
        datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
    response.set_cookie(
        key, value,
        max_age=max_age,
        expires=expires,
        domain=settings.SESSION_COOKIE_DOMAIN,
        secure=settings.SESSION_COOKIE_SECURE or None
    )

