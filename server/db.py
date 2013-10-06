import dataset
from parse import parse
import sys

filename = sys.argv[1]
db = dataset.connect("sqlite:///test.db")

tblmedicine = db["medicine"]
tblmedingred = db["medicineingredient"]
tblingredient = db["ingredient"]

ingredients = {}
hash = lambda x : unicode(x["ingredient"]) + unicode(x["unit"])

try:
    db.begin()
    for product in parse(filename):
        ingreds = product.pop("ingredients")
        prod_id = tblmedicine.insert(product)

        for ingred in ingreds:
            ihash = hash(ingred)
            strength = ingred.pop("strength") or None
            if ihash in ingredients:
                ingred_id = ingredients[ihash]
            else:
                ingred_id = tblingredient.insert(ingred)
                ingredients[ihash] = ingred_id
            tblmedingred.insert({"product" : prod_id, "ingredient" : ingred_id, "strength" : strength})
except:
    db.rollback()
    import traceback
    traceback.print_exc()
    sys.exit(1)
db.commit() 
