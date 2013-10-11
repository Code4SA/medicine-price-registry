import json
from django.http import HttpResponse, Http404
from mpr import models

def serialize_ingredient(ingredient, strength):
    return {
        "name" : ingredient.name,
        "unit" : ingredient.unit,
        "strength" : strength,
    }

def serialize_product(product):
    return {
        "regno" : product.regno,
        "schedule" : product.schedule,
        "name" : product.name,
        "dosage_form" : product.dosage_form,
        "pack_size" : product.pack_size,
        "num_packs" : product.num_packs,
        "sep" : product.sep,
        "is_generic" : product.is_generic,
        "ingredients" : [
            serialize_ingredient(pi.ingredient, pi.strength)
            for pi in product.product_ingredients.all()
        ]
    }
    

def api(request):
    ingredsearch = request.GET.get("ingredient", "").strip()

    if len(ingredsearch) < 3:
        raise Http404  

    ingredients = models.Ingredient.objects.filter(name__icontains=ingredsearch)

    products = set()
    for i in ingredients:
        products |= set(i.product_set.all())

    products = [serialize_product(p) for p in products]
    return HttpResponse(
        json.dumps(products, indent=4), mimetype="application/json"
    )

