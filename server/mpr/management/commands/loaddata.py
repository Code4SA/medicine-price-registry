import sys

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
import xlrd
from mpr import models

class Command(BaseCommand):
    args = '<filename>'
    help = "Populate database from mpr xls file"

    def parse(self, filename):

        workbook = xlrd.open_workbook(filename)
        worksheet = workbook.sheet_by_index(0)

        product = None
        for idx in range(2, worksheet.nrows):
            regno = worksheet.cell_value(idx, 2)
            if regno.strip() != "":
                if product: yield product
                
                generic_value = worksheet.cell_value(idx, 20) 
                name = worksheet.cell_value(idx, 6).title()
                if "originator" in generic_value.lower():
                    is_generic = "Originator"
                elif "generic" in generic_value.lower():
                    is_generic = "Generic"
                else:
                    is_generic = None

                product = {
                    "regno" : worksheet.cell_value(idx, 2).lower(),
                    "applicant" : worksheet.cell_value(idx, 1).title(),
                    "schedule" : worksheet.cell_value(idx, 5),
                    "name" : worksheet.cell_value(idx, 6).title(),
                    "dosage_form" : worksheet.cell_value(idx, 10).title(),
                    "pack_size" : worksheet.cell_value(idx, 11) or None,
                    "num_packs" : worksheet.cell_value(idx, 12) or None,
                    "sep" : worksheet.cell_value(idx, 16) or None,
                    "is_generic" : is_generic,
                    "ingredients" : []
                }

            product["ingredients"].append({
                "name" : worksheet.cell_value(idx, 7).title(),
                "strength" : worksheet.cell_value(idx, 8),
                "unit" : worksheet.cell_value(idx, 9).lower(),
            })

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
            count += 1
            sys.stdout.write(r"\r%s" % count)
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
