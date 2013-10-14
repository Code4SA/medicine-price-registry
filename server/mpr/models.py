from __future__ import division
from django.db import models

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=10)

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

    def search_by_product(self, pattern):

        products = Product.objects.filter(name__icontains=pattern).order_by("sep")
        return products

class Product(models.Model):
    regno = models.CharField(max_length=50, null=True)
    name = models.CharField(max_length=100)
    schedule = models.CharField(max_length=5, null=True)
    dosage_form = models.CharField(max_length=20, null=True)
    pack_size = models.FloatField(null=True)
    num_packs = models.IntegerField(null=True)
    sep = models.FloatField(null=True)
    is_generic = models.CharField(max_length=20, null=True)

    ingredients = models.ManyToManyField(Ingredient, through='ProductIngredient')

    objects = ProductManager()

    def __unicode__(self):
        return self.name

    @property
    def max_fee(self):
        try:
            if self.sep < 81:
                return self.sep * 1.46 + 6.3
            elif self.sep < 216:
                return self.sep * 1.33 + 16
            elif self.sep < 756:
                return self.sep * 1.15 + 52
            else:
                return self.sep * 1.05 + 123
        except (ValueError, TypeError):
            return self.sep

class ProductIngredient(models.Model):
    product = models.ForeignKey(Product, related_name="product_ingredients")
    ingredient = models.ForeignKey(Ingredient)
    strength = models.CharField(max_length=20)

    class Meta:
        unique_together = ("product", "ingredient", "strength")

    def __unicode__(self):
        return "%s %s" % (self.ingredient, self.strength)
