import sys
import logging
import csv

from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from django.db import transaction

from django.conf import settings

from dataprocessing.parsing import nappi

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    args = '<filename>'
    help = "Populate database from mediscor"
    # https://www.mediscor.co.za/search-medicine-reference-price/

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str)

    @transaction.atomic
    def handle(self, *args, **options):
        filename = options["filename"]

        nappi.parse(open(filename, encoding="latin1"))

