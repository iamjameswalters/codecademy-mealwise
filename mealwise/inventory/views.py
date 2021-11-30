from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from . import forms, models

# Home view

class HomeView(TemplateView):
  template_name = "inventory/home.html"
  extra_context = {'active_nav_home': "active"}

# List views

class Ingredients(ListView):
  template_name = "inventory/ingredients.html"
  model = models.Ingredient
  extra_context = {'active_nav_pantry': "active"}

class Menu(ListView):
  template_name = "inventory/menu.html"
  model = models.MenuItem
  extra_context = {'active_nav_menu': "active"}

class RecipeRequirements(ListView):
  template_name = "inventory/recipe_requirements.html"
  model = models.RecipeRequirement
  extra_context = {'active_nav_recipes': "active"}

class Purchases(ListView):
  template_name = "inventory/purchases.html"
  model = models.Purchase
  extra_context = {'active_nav_purchases': "active"}

# Create Views

class CreateIngredient(CreateView):
  template_name = "inventory/create_ingredient.html"
  model = models.Ingredient
  form_class = forms.IngredientForm
  extra_context = {'active_nav_pantry': "active"}

class CreateMenuItem(CreateView):
  template_name = "inventory/create_menu_item.html"
  model = models.MenuItem
  form_class = forms.MenuItemForm
  extra_context = {'active_nav_menu': "active"}

class CreateRecipeRequirement(CreateView):
  template_name = "inventory/create_recipe_req.html"
  model = models.RecipeRequirement
  form_class = forms.RecipeRequirementForm
  extra_context = {'active_nav_recipes': "active"}

class CreatePurchase(CreateView):
  template_name = "inventory/create_purchase.html"
  model = models.Purchase
  form_class = forms.PurchaseForm
  extra_context = {'active_nav_purchases': "active"}

# Update Views

class UpdateIngredient(UpdateView):
  template_name = "inventory/update_ingredient.html"
  model = models.Ingredient
  form_class = forms.IngredientForm
  extra_context = {'active_nav_pantry': "active"}

class UpdateMenuItem(UpdateView):
  template_name = "inventory/update_menu_item.html"
  model = models.MenuItem
  form_class = forms.MenuItemForm
  extra_context = {'active_nav_menu': "active"}

class UpdateRecipeRequirement(UpdateView):
  template_name = "inventory/update_recipe_req.html"
  model = models.RecipeRequirement
  form_class = forms.RecipeRequirementForm
  extra_context = {'active_nav_recipes': "active"}

class UpdatePurchase(UpdateView):
  template_name = "inventory/update_purchase.html"
  model = models.Purchase
  form_class = forms.PurchaseForm
  extra_context = {'active_nav_purchases': "active"}

# Delete Views

class DeleteIngredient(DeleteView):
  template_name = "inventory/delete_ingredient.html"
  model = models.Ingredient
  success_url = "/ingredients"
  extra_context = {'active_nav_pantry': "active"}

class DeleteMenuItem(DeleteView):
  template_name = "inventory/delete_menu_item.html"
  model = models.MenuItem
  success_url = "/menu"
  extra_context = {'active_nav_menu': "active"}

class DeleteRecipeRequirement(DeleteView):
  template_name = "inventory/delete_recipe_req.html"
  model = models.RecipeRequirement
  success_url = "/recipes"
  extra_context = {'active_nav_recipes': "active"}

class DeletePurchase(DeleteView):
  template_name = "inventory/delete_purchase.html"
  model = models.Purchase
  success_url = "/purchases"
  extra_context = {'active_nav_purchases': "active"}