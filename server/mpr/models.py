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
    def related_products(self):
        iq = models.Q()
        for pi in self.product_ingredients.all():
            iq &= models.Q(product_ingredients__ingredient=pi.ingredient, product_ingredients__strength=pi.strength)

        return Product.objects.filter(iq)

    @property
    def max_fee(self):
        VAT = 1.14
        try:
            if self.sep < 81:
                return self.sep + (self.sep * 0.46 + 6.3) * VAT
            elif self.sep < 216:
                return self.sep + (self.sep * 0.33 + 16) * VAT
            elif self.sep < 756:
                return self.sep + (self.sep * 0.15 + 52) * VAT
            else:
                return self.sep + (self.sep * 0.05 + 123) * VAT
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
