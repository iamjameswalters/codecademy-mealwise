from django import forms
from . import models

class MenuItemForm(forms.ModelForm):
  class Meta:
    model = models.MenuItem
    fields = "__all__"

class RecipeRequirementForm(forms.ModelForm):
  class Meta:
    model = models.RecipeRequirement
    fields = "__all__"

class IngredientForm(forms.ModelForm):
  class Meta:
    model = models.Ingredient
    fields = "__all__"

class PurchaseForm(forms.ModelForm):
  class Meta:
    model = models.Purchase
    fields = "__all__"
