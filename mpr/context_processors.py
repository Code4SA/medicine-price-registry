from django.conf import settings

from .models import LastUpdated

def settings_context(request):
    context = {}

    try:
        last_updated = LastUpdated.objects.all().order_by('-update_date')[0]
        context['last_updated'] = last_updated
    except IndexError:
        context['last_updated'] = u"Never"

    context['price_parameters'] = settings.PRICE_PARAMETERS
    context['latest_gazette'] = getattr(settings, "LATEST_GAZETTE", None)

    return context
