import sys
import logging

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
import xlrd
from mpr import models

from dataprocessing.parsing import nappi

name_change = {
    "amoxycillin" : "Amoxicillin",
}


logger = logging.getLogger(__name__)

class ConversionLogger:
    def __init__(self):
        self.logs = {}

    def log(self):
        pass

def clean_unit(unit):
    unit = unit.strip()
    lunit = unit.lower()
    skip_patterns = [
        "at reference date",
        "antigen units",
        "elisa units",
        "d-antigen unit",
    ]

    for s in skip_patterns:
        if s in lunit:
            return unit

    return unit.replace(" ", "")

def fix_product_unit(nappi_code, ingredient, unit):
    unit = clean_unit(unit)
    fixes = {
        "702983003": {
            "Timolol": {
                "unit": "mg/ml",
            }
        },
        "720983001": {
            "Dorzolamide": {
                "unit": "mg/ml",
            }
        },
    }

    if nappi_code in fixes and ingredient in fixes[nappi_code]:
        unit = fixes[nappi_code][ingredient]["unit"]

    return unit

def fix_ingredient_name(nappi_code, ingredient):
    fixes = {
        "722712001": {
            "Timilol": "Timolol"
        }
    }

    if nappi_code in fixes and ingredient in fixes[nappi_code]:
        return fixes[nappi_code][ingredient]

    return ingredient


class Command(BaseCommand):
    args = '<filename>'
    help = "Populate database from mpr xls file"

    @staticmethod
    def process_row(idx, extract_func):
        def clean_float(x, check_blank_is_1=False):
            try:
                if type(x) == float:
                    return x
                x = remove_dup_decimal(x)
                x = x.replace(" ", "")
                if check_blank_is_1:
                    x = blank_is_1(x)
                return float(x)
            except ValueError:
                return None

        def remove_dup_decimal(x):
            if x.count(".") > 1:
                x = "".join(x.split(".", 1))
            return x

        def blank_is_1(x):
            if x.strip() == "":
                return 1
            return x

        def to_empty(x):
            if x is None:
                return ""
            else:
                return x

        to_empty(extract_func(idx, 1)).title(),
        extract_func(idx, 2).lower(),
        extract_func(idx, 3),
        extract_func(idx, 5),
        extract_func(idx, 6).title(),
        to_empty(extract_func(idx, 10)).title(),
        clean_float(extract_func(idx, 11)),
        clean_float(extract_func(idx, 12), check_blank_is_1=True),
        clean_float(extract_func(idx, 16)),
        extract_func(idx, 20)

        sep = clean_float(extract_func(idx, 16))
        name = extract_func(idx, 6).title()
        pack_size = clean_float(extract_func(idx, 11))
        num_packs = clean_float(extract_func(idx, 12), check_blank_is_1=True)

        if sep is None:
            logger.warning(f"Skipping {name} as it is missing an SEP")
        elif pack_size is None:
            logger.warning(f"Skipping {name} as it is missing a pack_size")
        elif num_packs is None:
            logger.warning(f"Skipping {name} as it is missing num_packs")
            return

        return {
            "applicant": to_empty(extract_func(idx, 1)).title(),
            "regno": extract_func(idx, 2).lower(),
            "nappi_code": str(int(extract_func(idx, 3))),
            "schedule": extract_func(idx, 5),
            "name": name,
            "dosage_form": to_empty(extract_func(idx, 10)).title(),
            "pack_size": pack_size,
            "num_packs": num_packs,
            "sep": sep,
            "is_generic": "Originator" if extract_func(idx, 20) == "originator" else  "Generic"
        }

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str)

    def parse(self, filename):
        workbook = xlrd.open_workbook(filename)
        worksheet = workbook.sheet_by_index(0)

        product = None
        for idx in range(1, worksheet.nrows):
            try:
                regno = worksheet.cell_value(idx, 2).lower()
                if "medicine" in regno:
                    continue

                if regno.strip() != "":
                    if product is not None:
                        yield product

                    product = Command.process_row(idx, worksheet.cell_value)
                    if product is None:
                        continue

                    product["ingredients"] = []

                if product is None:
                    continue


                ingredient_name = worksheet.cell_value(idx, 7).title()
                product["ingredients"].append({
                    "name" : name_change.get(ingredient_name.lower(), ingredient_name),
                    "strength" : worksheet.cell_value(idx, 8),
                    "unit" : worksheet.cell_value(idx, 9).lower(),
                })

            except ValueError as e:
                import traceback; traceback.print_exc()
                print(e)
                print(worksheet.cell_value(idx, 2))

        if product: yield product
                


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
        fixed_name_count = 0
        filename = options["filename"]

        self.delete_products()

        logger.info("Loading up nappi codes")
        nappi_lookup = nappi.nappi_lookup()

        logger.info("Loading up sep file")
        for idx, p in enumerate(self.parse(filename)):
            if idx % 100 == 0:
                sys.stdout.write("\r%s" % idx)
                sys.stdout.flush()

            nappi_code = p["nappi_code"]

            if p["nappi_code"] in nappi_lookup:
                nappi_product = nappi_lookup[nappi_code]
                if nappi_product["description"] != p["name"]:
                    fixed_name_count += 1

                p["name"] = nappi_product["description"]

                if nappi_product["form"].strip() != "":
                    p["dosage_form"] = nappi_product["form"]

            sep = float_or_none(p["sep"])
            num_packs = int_or_none(p["num_packs"])
            pack_size = int_or_none(p["pack_size"])
            if None in [sep, num_packs, pack_size]:
                continue

            product = models.Product.objects.create(
                nappi_code=p["nappi_code"],
                name=p["name"], regno=p["regno"], schedule=p["schedule"],
                dosage_form=p["dosage_form"], pack_size=pack_size, num_packs=num_packs,
                sep=sep, is_generic=p["is_generic"]
            )

            for i in p["ingredients"]:
                ingredient_name = fix_ingredient_name(p["nappi_code"], i["name"])
                unit = fix_product_unit(p["nappi_code"], ingredient_name, i["unit"])
                ingredient, _ = models.Ingredient.objects.get_or_create(name=ingredient_name, unit=unit)
                models.ProductIngredient.objects.get_or_create(
                    product=product, ingredient=ingredient, strength=i["strength"]
                )
        models.LastUpdated.objects.create()
        logger.info(f"Corrected {fixed_name_count} names")
