from .import serialisers
from . import models
from .packageinserts import packageinserts
from . import apiv2

def product_detail(nappi_code, serialiser=serialisers.serialize_product_apiv3):
    return apiv2.product_detail(nappi_code, serialisers.serialize_product_apiv3)
