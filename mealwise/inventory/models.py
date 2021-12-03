from django.db import models

# Create your models here.
class Ingredient(models.Model):
    name = models.CharField(max_length=50, unique=True)
    quantity = models.FloatField(default=0)
    unit = models.CharField(max_length=15)
    price_per_unit = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def __str__(self):
        return "{name} ingredient, quantity: {quan} {unit}(s)".format(name=self.name, quan=self.quantity, unit=self.unit)

    def get_absolute_url(self):
        return "/ingredients"

class MenuItem(models.Model):
    name = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)

    def __str__(self):
        return "{item}: ${price}".format(item=self.name, price=self.price)

    def get_absolute_url(self):
        return "/menu"

    def is_available(self):
        for ingredient in self.reciperequirement_set.all():
            if not ingredient.enough():
                return False
        return True

class RecipeRequirement(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0)

    class Meta:
        unique_together = (('menu_item', 'ingredient'),)

    def __str__(self):
        return "Recipe: {menu} requires {quan} {unit}(s) of {ing}".format(ing=self.ingredient.name, menu=self.menu_item.name, quan=self.quantity, unit=self.ingredient.unit)

    def get_absolute_url(self):
        return "/recipes"

    def enough(self):
        return self.ingredient.quantity >= self.quantity

class Purchase(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Order for {item} at {time}".format(item=self.menu_item.name, time=self.time)

    def get_absolute_url(self):
        return "/purchases"