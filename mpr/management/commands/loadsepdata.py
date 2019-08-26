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

    @staticmethod
    def process_row(idx, extract_func):
        def to_empty(x):
            if x is None:
                return ""
            else:
                return x

        return {
            "applicant": to_empty(extract_func(idx, 1)).title(),
            "regno": extract_func(idx, 2).lower(),
            "nappi_code": int(extract_func(idx, 3)),
            "schedule": extract_func(idx, 5),
            "name": extract_func(idx, 6).title(),
            "dosage_form": to_empty(extract_func(idx, 10)).title(),
            "pack_size": float(extract_func(idx, 11)),
            "num_packs": float(extract_func(idx, 12)),
            "sep": float(extract_func(idx, 16)),
            "is_generic": "Originator" if extract_func(idx, 20) == "originator" else  "Generic"
        }

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str)

    def parse(self, filename):
        workbook = xlrd.open_workbook(filename)
        worksheet = workbook.sheet_by_index(0)

        product = None
        for idx in range(1, worksheet.nrows):
            product = Command.process_row(idx, worksheet.cell_value)

            if "medicine" in product["regno"]:
                continue

            if product["regno"].strip() != "":
                if product: yield product
                
                product["ingredients"] = []

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

    @transaction.atomic
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
        filename = options["filename"]

        self.delete_products()

        count += 1
        sys.stdout.write(r"\r%s" % count)
        sys.stdout.flush()
        if count % 100 == 0: sys.stdout.flush()
        for p in self.parse(filename):
            product = models.Product.objects.create(
                nappi_code=p["nappi_code"],
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
