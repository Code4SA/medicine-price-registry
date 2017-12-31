from __future__ import division
from django.db import models

class Ingredient(models.Model):
    name = models.CharField(max_length=250)
    unit = models.CharField(max_length=20)

    class Meta:
        unique_together = ("name", "unit")

    def __unicode__(self):
        return self.name

class ProductManager(models.Manager):
    def search_by_ingredient(self, pattern):

        ingredients = Ingredient.objects.filter(name__icontains=pattern)

        products = set()
        for i in ingredients:
            products |= set(i.product_set.all())

        products = sorted(products, key=lambda x: x.sep)
        return products

    def search_by_nappi(self, nappi):

        products = Product.objects.filter(nappi_code=nappi).order_by("sep")
        return products

    def search_by_product_name(self, pattern):

        products = Product.objects.filter(name__icontains=pattern).order_by("sep")
        return products

class Product(models.Model):
    nappi_code = models.CharField(max_length=20, null=False)
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

    def __unicode__(self):
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
        return self.dispensing_fee + self.sep

    @property
    def dispensing_fee(self):
        VAT = 1.14
        try:
            if self.sep < 107.15:
                return (self.sep * 0.46 + 11.25) * VAT
            elif self.sep < 285.8:
                return (self.sep * 0.33 + 24) * VAT
            elif self.sep < 1000.33:
                return (self.sep * 0.15 + 73.5) * VAT
            else:
                return (self.sep * 0.05 + 172) * VAT
        except (ValueError, TypeError):
            return self.sep

    @property
    def cost_per_unit(self):
        if self.pack_size > 0:
            qty = self.pack_size * self.num_packs
        else:
            qty = self.num_packs
        return self.max_fee / qty

class ProductIngredient(models.Model):
    product = models.ForeignKey(Product, related_name="product_ingredients")
    ingredient = models.ForeignKey(Ingredient)
    strength = models.CharField(max_length=20)

    class Meta:
        unique_together = ("product", "ingredient", "strength")

    def __unicode__(self):
        return "%s %s" % (self.ingredient, self.strength)

class LastUpdatedManager(models.Manager):
    def last_updated(self):
        return LastUpdated.objects.all().order_by('-update_date')[0]

class LastUpdated(models.Model):
    update_date = models.DateField(auto_now_add=True)
    objects = LastUpdatedManager()

    def __unicode__(self):
        return str(self.update_date)

