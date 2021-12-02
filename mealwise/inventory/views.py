from decimal import Decimal
from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from . import forms, models

# Robots.txt view

class Robots(TemplateView):
  template_name = "robots.txt"
  content_type = "text/plain"

# Account Creation view

class CreateAccount(CreateView):
  form_class = UserCreationForm
  success_url = reverse_lazy("login")
  template_name = 'registration/signup.html'

# Home view

class HomeView(TemplateView):
  template_name = "inventory/home.html"
  extra_context = {'active_nav_home': "active"}

# Report view

class ReportView(LoginRequiredMixin, TemplateView):
  template_name = "inventory/report.html"

  def get_context_data(self, **kwargs):
    # Run default context method first
    context = super().get_context_data(**kwargs)
    
    # Create purchase queryset
    purchase_queryset = models.Purchase.objects.all()

    # Calculate revenue
    total_revenue = Decimal()
    for purchase in purchase_queryset:
      total_revenue += purchase.menu_item.price
    context['revenue'] = total_revenue
    
    # Calculate costs
    cost = Decimal()
    for purchase in purchase_queryset:
      ingredients_cost = Decimal()
      recipe = purchase.menu_item.reciperequirement_set.all()
      for recipe_requirement in recipe:
        ingredient_cost = recipe_requirement.ingredient.price_per_unit
        quantity = Decimal(recipe_requirement.quantity)
        ingredients_cost += ingredient_cost * quantity
      cost += ingredients_cost
    context['costs'] = cost

    # Calculate profit
    profit = total_revenue - cost
    context['profit'] = profit

    # Add active navbar class
    context['active_nav_report'] = 'active'

    return context

# List views

class Ingredients(LoginRequiredMixin, ListView):
  template_name = "inventory/ingredients.html"
  model = models.Ingredient
  extra_context = {'active_nav_pantry': "active"}

class Menu(ListView):
  template_name = "inventory/menu.html"
  model = models.MenuItem
  extra_context = {'active_nav_menu': "active"}

class RecipeRequirements(LoginRequiredMixin, ListView):
  template_name = "inventory/recipe_requirements.html"
  model = models.RecipeRequirement
  extra_context = {'active_nav_recipes': "active"}

class Purchases(ListView):
  template_name = "inventory/purchases.html"
  model = models.Purchase
  extra_context = {'active_nav_purchases': "active"}

# Create Views

class CreateIngredient(LoginRequiredMixin, CreateView):
  template_name = "inventory/create_ingredient.html"
  model = models.Ingredient
  form_class = forms.IngredientForm
  extra_context = {'active_nav_pantry': "active"}

class CreateMenuItem(LoginRequiredMixin, CreateView):
  template_name = "inventory/create_menu_item.html"
  model = models.MenuItem
  form_class = forms.MenuItemForm
  extra_context = {'active_nav_menu': "active"}

class CreateRecipeRequirement(LoginRequiredMixin, CreateView):
  template_name = "inventory/create_recipe_req.html"
  model = models.RecipeRequirement
  form_class = forms.RecipeRequirementForm
  extra_context = {'active_nav_recipes': "active"}

class CreatePurchase(CreateView):
  template_name = "inventory/create_purchase.html"
  model = models.Purchase
  form_class = forms.PurchaseForm

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)

    full_menu = models.MenuItem.objects.all()
    context['available_items'] = [item for item in full_menu if item.is_available()]
    context['active_nav_purchases'] = 'active'

    return context

  def post(self, request):
    purchase_item_id = request.POST['menu_item']
    purchase_item = models.MenuItem.objects.get(pk=purchase_item_id)
    for recipe_req in purchase_item.reciperequirement_set.all():
      purchase_ingredient = recipe_req.ingredient
      purchase_ingredient.quantity -= recipe_req.quantity
      purchase_ingredient.save()
    purchase = models.Purchase(menu_item=purchase_item)
    purchase.save()
    return redirect("/purchases")

# Update Views

class UpdateIngredient(LoginRequiredMixin, UpdateView):
  template_name = "inventory/update_ingredient.html"
  model = models.Ingredient
  form_class = forms.IngredientForm
  extra_context = {'active_nav_pantry': "active"}

class UpdateMenuItem(LoginRequiredMixin, UpdateView):
  template_name = "inventory/update_menu_item.html"
  model = models.MenuItem
  form_class = forms.MenuItemForm
  extra_context = {'active_nav_menu': "active"}

class UpdateRecipeRequirement(LoginRequiredMixin, UpdateView):
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

class DeleteIngredient(LoginRequiredMixin, DeleteView):
  template_name = "inventory/delete_ingredient.html"
  model = models.Ingredient
  success_url = "/ingredients"
  extra_context = {'active_nav_pantry': "active"}

class DeleteMenuItem(LoginRequiredMixin, DeleteView):
  template_name = "inventory/delete_menu_item.html"
  model = models.MenuItem
  success_url = "/menu"
  extra_context = {'active_nav_menu': "active"}

class DeleteRecipeRequirement(LoginRequiredMixin, DeleteView):
  template_name = "inventory/delete_recipe_req.html"
  model = models.RecipeRequirement
  success_url = "/recipes"
  extra_context = {'active_nav_recipes': "active"}

class DeletePurchase(DeleteView):
  template_name = "inventory/delete_purchase.html"
  model = models.Purchase
  success_url = "/purchases"
  extra_context = {'active_nav_purchases': "active"}