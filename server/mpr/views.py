import json
from django.http import HttpResponse, Http404
from mpr import models
import serialisers

def api(request):
    ingredsearch = request.GET.get("ingredient", "").strip()

    if len(ingredsearch) < 3:
        products = []
    else:
        ingredients = models.Ingredient.objects.filter(name__icontains=ingredsearch)

        products = set()
        for i in ingredients:
            products |= set(i.product_set.all())

        products = sorted(products, key=lambda x: x.sep)
        products = [serialisers.serialize_product(p) for p in products]

    return HttpResponse(
        json.dumps(products, indent=4), mimetype="application/json"
    )

