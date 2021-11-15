from django import forms
from . import models

class MenuItemForm(forms.modelForm):
  class Meta:
    model = models.MenuItem
    fields = "__all__"

class RecipeRequirementForm(forms.modelForm):
  class Meta:
    model = models.RecipeRequirement
    fields = "__all__"

class IngredientForm(forms.modelForm):
  class Meta:
    model = models.Ingredient
    fields = "__all__"

class PurchaseForm(forms.modelForm):
  class Meta:
    model = models.Purchase
    fields = "__all__"
