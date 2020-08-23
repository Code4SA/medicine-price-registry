import sys
import logging
import csv

from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from django.db import transaction

from django.conf import settings

from mpr import models

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    args = '<filename>'
    help = "Populate database from mediscor"
    # https://www.mediscor.co.za/search-medicine-reference-price/

    def add_arguments(self, parser):
        parser.add_argument('formulary', type=str)
        parser.add_argument('filename', type=str)

    @transaction.atomic
    def handle(self, *args, **options):
        params = settings.PRICE_PARAMETERS
        VAT = params["VAT"]
        formulary_name = options["formulary"]
        filename = options["filename"]

        formulary, _ = models.Formulary.objects.get_or_create(name=formulary_name)
        formulary.save()
        models.FormularyProduct.objects.filter(formulary=formulary).delete()

        for row in csv.DictReader(open(filename)):
            nappi_code = f"{row['Nappi Code']}{row['Nappi Ext']}"
            try:
                product = models.Product.objects.get(nappi_code=nappi_code)
                if product.pack_size is None:
                    logger.warning(f"Skipping product without a pack size: {nappi_code}")
                    continue
                different_size = float(product.pack_size) != float(row["Pack Size"])
                if (different_size):
                    # print(f"Different: {nappi_code} - {product.pack_size} Data: {row['Pack Size']}")
                    logger.warning(f"Found product with different pack size - skipping: {nappi_code}")
                else:
                    max_price = float(row["MRP (Excl Vat)"]) * VAT * product.pack_size
                    models.FormularyProduct.objects.update_or_create(formulary=formulary, product=product, defaults={"price": max_price})
                    print(nappi_code)
            except models.Product.DoesNotExist:
                logger.warning(f"Could not find product with NAPPI code: {nappi_code}")
            except models.Product.MultipleObjectsReturned:
                logger.warning(f"Multiple products with the same NAPPI code: {nappi_code}")
