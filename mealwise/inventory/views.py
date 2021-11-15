from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from . import models

# Create your views here.
class HomeView(TemplateView):
  template_name = "inventory/home.html"
  context = {}

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
