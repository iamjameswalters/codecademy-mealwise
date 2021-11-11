from django.db import models

# Create your models here.
class Ingredient(models.Model):
    name = models.CharField(max_length=50, unique=True)
    quantity = models.IntegerField(max_length=3, default=0)
    unit = models.CharField(max_length=15)
    price_per_unit = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def __str__(self):
        return "{} ingredient".format(self.name)

class MenuItem(models.Model):
    name = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)

    def __str__(self):
        return "{} menu item".format(self.name)

class RecipeRequirement(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity_required = models.FloatField(default=0)

    def __str__(self):
        return "{ing} requirement for {menu}".format(ing=self.ingredient.name, menu=self.menu_item.name)

class Purchase(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Order for {}".format(self.menu_item.name)