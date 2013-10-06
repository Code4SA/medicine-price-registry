import dataset

db = dataset.connect("sqlite:///test.db")

tblmedicine = db["medicine"]
tblmedingred = db["medicineingredient"]
tblingredient = db["ingredient"]

query = "lamotrigine".title()
paracetamol = tblingredient.find_one(ingredient=query)
medingred = tblmedingred.find(ingredient=paracetamol["id"])
for m in medingred:
    prod_id = m["product"]
    product = tblmedicine.find_one(id=prod_id)
    print "%(sep)f %(name)s %(pack size)d %(quantity)d %(dosage form)s %(sep)f" % product
