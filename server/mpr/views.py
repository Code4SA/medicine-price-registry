import json
from django.http import HttpResponse, Http404
from mpr import models

def as_currency(x):
    x = float(x)
    return "R %.2f" % x

dosage_form = {
    "Liq" : "liquid",
    "Tab" : "tablet",
    "Cap" : "capsule",
    "Oin" : "ointment",
    "Lit" : "lotion",
    "Inj" : "injection",
    "Syr" : "syrup",
    "Eft" : "Effervescent",
    "Drp" : "Drops",
    "Sus" : "Suspension",
    "Cal" : "Calasthetic",
    "Sol" : "Solution",
    "Neb" : "Nebuliser",
    "Inh" : "Inhaler",
    "Inf" : "Infusion",
}

def int_or_float(x):
    try:
        x = float(x)
        if int(x) == float(x):
            return int(x)
        return x
    except (ValueError, TypeError):
        return "-"

def serialize_ingredient(ingredient, strength):
    return {
        "name" : ingredient.name,
        "unit" : ingredient.unit,
        "strength" : int_or_float(strength),
    }

def serialize_product(product):
    return {
        "regno" : product.regno,
        "schedule" : product.schedule,
        "name" : product.name,
        "dosage_form" : dosage_form.get(product.dosage_form, product.dosage_form),
        "pack_size" : product.pack_size,
        "num_packs" : product.num_packs,
        "sep" : as_currency(product.sep),
        "is_generic" : product.is_generic,
        "ingredients" : [
            serialize_ingredient(pi.ingredient, pi.strength)
            for pi in product.product_ingredients.all()
        ]
    }
    

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
        products = [serialize_product(p) for p in products]

    return HttpResponse(
        json.dumps(products, indent=4), mimetype="application/json"
    )

