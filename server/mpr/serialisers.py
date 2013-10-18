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

def as_currency(x):
    try:
        x = float(x)
        return "R %.2f" % x
    except (ValueError, TypeError):
        return "-"

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
        "id" : product.id,
        "regno" : product.regno,
        "schedule" : product.schedule,
        "name" : product.name,
        "dosage_form" : dosage_form.get(product.dosage_form, product.dosage_form),
        "pack_size" : product.pack_size,
        "num_packs" : product.num_packs,
        "sep" : as_currency(product.max_fee),
        "is_generic" : product.is_generic,
        "ingredients" : [
            serialize_ingredient(pi.ingredient, pi.strength)
            for pi in product.product_ingredients.all()
        ]
    }

def serialize_products(products):
    return [serialize_product(p) for p in products]
