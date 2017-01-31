import sys

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
import xlrd
from mpr import models

name_change = {
    "amoxycillin" : "Amoxicillin",
}

class Command(BaseCommand):
    args = '<filename>'
    help = "Populate database from mpr xls file"

    def parse(self, filename):

        workbook = xlrd.open_workbook(filename)
        worksheet = workbook.sheet_by_index(0)

        product = None
        for idx in range(1, worksheet.nrows):
            regno = worksheet.cell_value(idx, 2).lower()
            pack_size = worksheet.cell_value(idx, 11)
            num_packs = worksheet.cell_value(idx, 12)
            sep = worksheet.cell_value(idx, 16)
            name = worksheet.cell_value(idx, 6).title()

            if "medicine" in regno.lower():
                continue

            if regno.strip() != "":
                if product: yield product
                
                generic_value = worksheet.cell_value(idx, 20) 
                if "originator" in generic_value.lower():
                    is_generic = "Originator"
                elif "generic" in generic_value.lower():
                    is_generic = "Generic"
                else:
                    is_generic = None

                if not sep:
                    print "Could not process %s (%s) due to lack of SEP" % (name, regno)
                    continue
                pack_size = pack_size or 1
                num_packs = num_packs or 1

                product = {
                    "regno" : regno,
                    "applicant" : worksheet.cell_value(idx, 1).title(),
                    "schedule" : worksheet.cell_value(idx, 5),
                    "name" : name,
                    "dosage_form" : worksheet.cell_value(idx, 10).title(),
                    "pack_size" : pack_size,
                    "num_packs" : num_packs,
                    "sep" : sep,
                    "is_generic" : is_generic,
                    "ingredients" : []
                }

            ingredient_name = worksheet.cell_value(idx, 7).title()
            product["ingredients"].append({
                "name" : name_change.get(ingredient_name.lower(), ingredient_name),
                "strength" : worksheet.cell_value(idx, 8),
                "unit" : worksheet.cell_value(idx, 9).lower(),
            })

    def delete_products(self):
        while models.Product.objects.count():
            ids = models.Product.objects.values_list('pk', flat=True)[:100]
            models.Product.objects.filter(pk__in = ids).delete()

    def handle(self, *args, **options):
        def int_or_none(x):
            try:
                return int(x)
            except (ValueError, TypeError):
                return None

        def float_or_none(x):
            try:
                return float(x)
            except (ValueError, TypeError):
                return None

        count = 0
        filename = args[0]
        with transaction.commit_on_success():
            self.delete_products()

            count += 1
            sys.stdout.write(r"\r%s" % count)
            sys.stdout.flush()
            if count % 100 == 0: sys.stdout.flush()
            for p in self.parse(filename):
                product = models.Product.objects.create(
                    name=p["name"], regno=p["regno"], schedule=p["schedule"],
                    dosage_form=p["dosage_form"], pack_size=int_or_none(p["pack_size"]), num_packs=int_or_none(p["num_packs"]),
                    sep=float_or_none(p["sep"]), is_generic=p["is_generic"]
                )

                for i in p["ingredients"]:
                    ingredient, _ = models.Ingredient.objects.get_or_create(name=i["name"], unit=i["unit"])
                    models.ProductIngredient.objects.get_or_create(
                        product=product, ingredient=ingredient, strength=i["strength"]
                    )
            models.LastUpdated.objects.create()
