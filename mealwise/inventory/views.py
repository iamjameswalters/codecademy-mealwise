from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from . import forms, models

# Home view

class HomeView(TemplateView):
  template_name = "inventory/home.html"
  context = {}

# List views

class Ingredients(ListView):
  template_name = "inventory/ingredients.html"
  model = models.Ingredient

class Menu(ListView):
  template_name = "inventory/menu.html"
  model = models.MenuItem

class RecipeRequirements(ListView):
  template_name = "inventory/recipe_requirements.html"
  model = models.RecipeRequirement

class Purchases(ListView):
  template_name = "inventory/purchases.html"
  model = models.Purchase

# Create Views

class CreateIngredient(CreateView):
  template_name = "inventory/create_ingredient.html"
  model = models.Ingredient
  form_class = forms.IngredientForm

class CreateMenuItem(CreateView):
  template_name = "inventory/create_menu_item.html"
  model = models.MenuItem
  form_class = forms.MenuItemForm

class CreateRecipeRequirement(CreateView):
  template_name = "inventory/create_recipe_req.html"
  model = models.RecipeRequirement
  form_class = forms.RecipeRequirementForm

class CreatePurchase(CreateView):
  template_name = "inventory/create_purchase.html"
  model = models.Purchase
  form_class = forms.PurchaseForm

# Update Views

class UpdateIngredient(UpdateView):
  template_name = "inventory/update_ingredient.html"
  model = models.Ingredient
  form_class = forms.IngredientForm

class UpdateMenuItem(UpdateView):
  template_name = "inventory/update_menu_item.html"
  model = models.MenuItem
  form_class = forms.MenuItemForm

class UpdateRecipeRequirement(UpdateView):
  template_name = "inventory/update_recipe_req.html"
  model = models.RecipeRequirement
  form_class = forms.RecipeRequirementForm

class UpdatePurchase(UpdateView):
  template_name = "inventory/update_purchase.html"
  model = models.Purchase
  form_class = forms.PurchaseForm

# Delete Views

class DeleteIngredient(DeleteView):
  template_name = "inventory/delete_ingredient.html"
  model = models.Ingredient
  success_url = "/ingredients"

class DeleteMenuItem(DeleteView):
  template_name = "inventory/delete_menu_item.html"
  model = models.MenuItem
  success_url = "/menu"

class DeleteRecipeRequirement(DeleteView):
  template_name = "inventory/delete_recipe_req.html"
  model = models.RecipeRequirement
  success_url = "/recipes"

class DeletePurchase(DeleteView):
  template_name = "inventory/delete_purchase.html"
  model = models.Purchase
  success_url = "/purchases"