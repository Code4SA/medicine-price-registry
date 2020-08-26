from __future__ import division
from django.conf import settings
from django.db import models

class Ingredient(models.Model):
    name = models.CharField(max_length=250)
    unit = models.CharField(max_length=20)

    class Meta:
        unique_together = ("name", "unit")

    def __str__(self):
        return f"{self.name} ({self.unit})"


class ProductManager(models.Manager):
    def search_by_ingredient(self, pattern):

        ingredients = Ingredient.objects.filter(name__icontains=pattern)

        products = set()
        for i in ingredients:
            products |= set(i.product_set.all())

        with_prices = [product for product in products if product.sep is not None]

        products = sorted(with_prices, key=lambda x: x.sep)
        return products

    def search_by_nappi(self, nappi):

        products = Product.objects.filter(nappi_code=nappi).order_by("sep")
        return products

    def search_by_product_name(self, pattern):

        products = Product.objects.filter(name__icontains=pattern).order_by("sep")
        return products

class Product(models.Model):
    nappi_code = models.CharField(max_length=20, null=False, unique=True)
    regno = models.CharField(max_length=50, null=False)
    name = models.CharField(max_length=100)
    schedule = models.CharField(max_length=22, null=True)
    dosage_form = models.CharField(max_length=20, null=True)
    pack_size = models.FloatField(null=False)
    num_packs = models.IntegerField(null=False)
    sep = models.FloatField(null=False)
    is_generic = models.CharField(max_length=20, null=True)

    ingredients = models.ManyToManyField(Ingredient, through='ProductIngredient')

    objects = ProductManager()

    # wish this could be dependecy injection but it isn't clear how to do this with Django models
    @staticmethod
    def parameters():
        return settings.PRICE_PARAMETERS

    def __str__(self):
        return self.name

    @property
    def related_products(self):
        num_ingredients = len(self.product_ingredients.all())
        qs = Product.objects.annotate(models.Count("ingredients")).filter(ingredients__count=num_ingredients)
        for pi in self.product_ingredients.all():
            qs = qs.filter(product_ingredients__ingredient=pi.ingredient, product_ingredients__strength=pi.strength)

        return qs.order_by("sep")

    @property
    def max_fee(self):
        if self.dispensing_fee is None or self.sep is None:
            return 0
        return self.dispensing_fee + self.sep

    @property
    def dispensing_fee(self):
        params = Product.parameters()
        VAT = params["VAT"]
        try:
            for threshold, perc, flat_rate in params["prices"]:
                if self.sep < threshold:
                    return (self.sep * perc + flat_rate) * VAT
        except (ValueError, TypeError):
            return self.sep

    @property
    def cost_per_unit(self):
        if self.pack_size is None:
            return 0

        if self.pack_size > 0:
            qty = self.pack_size * self.num_packs
        else:
            qty = self.num_packs
        return self.max_fee / qty

    @property
    def min_cost_per_unit(self):
        if self.pack_size > 0:
            qty = self.pack_size * self.num_packs
        else:
            qty = self.num_packs
        return self.sep / qty

    @property
    def max_cost_per_unit(self):
        return self.cost_per_unit

    @property
    def copayments(self):
        return [
            {"formulary": fp.formulary.name, "copayment": fp.copayment}
            for fp in self.formularyproducts.all()
        ]

class ProductIngredient(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_ingredients")
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    strength = models.CharField(max_length=20)

    class Meta:
        unique_together = ("product", "ingredient", "strength")

    def __str__(self):
        return "%s %s" % (self.ingredient, self.strength)

class LastUpdatedManager(models.Manager):
    def last_updated(self):
        return LastUpdated.objects.all().order_by('-update_date')[0]

class LastUpdated(models.Model):
    update_date = models.DateField(auto_now_add=True)
    objects = LastUpdatedManager()

    def __str__(self):
        return str(self.update_date)

class Formulary(models.Model):
    name = models.CharField(max_length=255)
    last_updated = models.DateField()

    def __str__(self):
        return self.name

class FormularyProduct(models.Model):
    formulary = models.ForeignKey(Formulary, on_delete=models.CASCADE, related_name="products")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="formularyproducts")
    price = models.FloatField(null=False)

    @property
    def copayment(self):
        return max(self.product.max_fee - self.price, 0)

    class Meta:
        unique_together = ("formulary", "product")

