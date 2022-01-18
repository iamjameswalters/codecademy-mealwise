from bokeh.plotting import figure
from bokeh.embed import components
from decimal import Decimal
from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from . import forms, models

# Robots.txt view

class Robots(TemplateView):
  template_name = "robots.txt"
  content_type = "text/plain"

# Custom Login view

class CustomLoginView(LoginView):
  template_name = "registration/login.html"
  base_template = 'full_modal.html'

  def get(self, request, *args, **kwargs):
    if request.htmx:
      next_url = request.GET.get('next', '')
      self.extra_context = {'next_page': next_url, 'basetemplate': self.base_template}
      self.template_name = "htmx/login_modal.html"
    return super().get(self, request, *args, **kwargs)

  def post(self, request, *args, **kwargs):
    if not request.htmx:
      return super().post(self, request, *args, **kwargs)
    form = self.get_form()
    if form.is_valid():
      auth_login(self.request, form.get_user())
      response = HttpResponse()
      response['HX-Redirect'] = self.get_success_url()
    else:
      next_url = request.GET.get('next', '')
      self.extra_context = {'next_page': next_url, 'basetemplate': 'htmx.html'}
      self.template_name = "htmx/login_modal.html"
      response = self.form_invalid(form)
    return response

class IntermodalLoginView(CustomLoginView):
  base_template = 'htmx.html'

# Account Creation view

class CreateAccount(SuccessMessageMixin, CreateView):
  form_class = UserCreationForm
  success_url = reverse_lazy("login")
  success_message = "Successfully created your account."
  template_name = 'registration/signup.html'
  base_template = 'full_modal.html'
  back_function = 'close'

  def form_valid(self, form):
    super().form_valid(form)
    return HttpResponseRedirect(self.get_success_url() + '?next=' + self.extra_context['next_page'])

  def get(self, request, *args, **kwargs):
    if request.htmx:
      next_url = request.GET.get('next', '')
      self.template_name = 'htmx/signup_modal.html'
      self.extra_context = {'basetemplate': self.base_template, 'next_page': next_url, 'back_function': self.back_function}
    return super().get(self, request, *args, **kwargs)

  def post(self, request, *args, **kwargs):
    if request.htmx:
      next_url = request.GET.get('next', '')
      back_fx = request.GET.get('back', '')
      self.template_name = 'htmx/signup_modal.html'
      self.extra_context = {'basetemplate': 'htmx.html', 'next_page': next_url, 'back_function': back_fx}
      self.success_url = reverse_lazy('login_intermodal')
    return super().post(self, request, *args, **kwargs)

class IntermodalCreateAccount(CreateAccount):
  base_template = 'htmx.html'
  back_function = ''

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

    # Create plot
    plot = figure()#toolbar_location=None)
    plot.circle([1,2], [3,4])
    script, div = components(plot)
    context['chart'] = {'script': script, 'div': div}

    # Add active navbar class
    context['active_nav_report'] = 'active'

    return context

# List views

class Ingredients(LoginRequiredMixin, ListView):
  template_name = "inventory/ingredients.html"
  model = models.Ingredient
  extra_context = {'active_nav_pantry': "active"}

class HtmxIngredient(DetailView):
  template_name = 'htmx/ingredient.html'
  model = models.Ingredient

def htmx_get_ingredient_unit_view(request):
  selected_ingredient = request.GET['ingredient']
  if selected_ingredient == '':
    return HttpResponse('unit')
  ingredient_obj = models.Ingredient.objects.get(id=selected_ingredient)
  unit = ingredient_obj.unit
  return HttpResponse(unit)

class Menu(ListView):
  template_name = "inventory/menu-with-cards.html"
  model = models.MenuItem
  extra_context = {'active_nav_menu': "active"}

class RecipeRequirements(LoginRequiredMixin, ListView):
  template_name = "inventory/recipe_requirements.html"
  model = models.RecipeRequirement
  extra_context = {'active_nav_recipes': "active"}

class HtmxRecipeRequirement(DetailView):
  template_name = 'htmx/recipe_requirement.html'
  model = models.RecipeRequirement

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

class HtmxCreateIngredient(CreateIngredient):
  template_name = "htmx/create_ingredient_modal.html"
  base_template = "full_modal.html"

  def get_success_url(self):
    return "/ingredients"
  
  def get(self, request, *args, **kwargs):
    self.extra_context = {'basetemplate': self.base_template}
    return super().get(self, request, *args, **kwargs)

  def form_valid(self, form):
    self.object = form.save()
    response = HttpResponse()
    response['Hx-Redirect'] = self.get_success_url()
    return response

  def form_invalid(self, form):
    self.extra_context['basetemplate'] = 'htmx.html'
    return super().form_invalid(form)

class HtmxCreateIngredientFromMenuItem(HtmxCreateIngredient):
  template_name = "htmx/create_ing_from_menu_item_modal.html"
  success_url = reverse_lazy('htmx_create_recipe_req')

  def form_valid(self, form):
    self.object = form.save()
    response = HttpResponse()
    response['Hx-Trigger'] = "NewIngredientRefresh"
    response['Hx-Retarget'] = "#dummy"
    return response

class CreateMenuItem(LoginRequiredMixin, CreateView):
  template_name = "inventory/create_menu_item.html"
  model = models.MenuItem
  form_class = forms.MenuItemForm
  extra_context = {'active_nav_menu': "active"}

class HtmxCreateMenuItem(CreateMenuItem):
  template_name = "htmx/create_menu_item_modal.html"
  base_template = 'full_modal.html'

  def get(self, request, *args, **kwargs):
    self.extra_context = {'basetemplate': self.base_template}
    return super().get(self, request, *args, **kwargs)

  def form_valid(self, form):
    self.object = form.save()
    response = HttpResponse()
    response['Hx-Redirect'] = self.get_success_url()
    return response

  def form_invalid(self, form):
    self.extra_context['basetemplate'] = 'htmx.html'
    return super().form_invalid(form)

class CreateRecipeRequirement(LoginRequiredMixin, CreateView):
  template_name = "inventory/create_recipe_req.html"
  model = models.RecipeRequirement
  form_class = forms.RecipeRequirementForm
  extra_context = {'active_nav_recipes': "active"}

class HtmxCreateRecipeRequirement(CreateRecipeRequirement):
  template_name = "htmx/create_recipe_req.html"

  def get(self, request, *args, **kwargs):
    self.extra_context = {'current_menu_item': self.kwargs.get(self.pk_url_kwarg)}
    return super().get(self, request, *args, **kwargs)

  def post(self, request, *args, **kwargs):
    self.extra_context = {'current_menu_item': self.kwargs.get(self.pk_url_kwarg)}
    return super().post(self, request, *args, **kwargs)

  def get_success_url(self):
    return reverse('htmx_recipe_req', args=(self.object.pk,))

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

  def post(self, request, *args, **kwargs):
    purchase_item_id = request.POST['menu_item']
    purchase_item = models.MenuItem.objects.get(pk=purchase_item_id)
    for recipe_req in purchase_item.reciperequirement_set.all():
      purchase_ingredient = recipe_req.ingredient
      purchase_ingredient.quantity -= recipe_req.quantity
      purchase_ingredient.save()
    purchase = models.Purchase(menu_item=purchase_item)
    purchase.save()
    if request.htmx:
      response = HttpResponse()
      response['Hx-Redirect'] = "/purchases"
      return response
    else:
      return redirect("/purchases")

class HtmxCreatePurchase(CreatePurchase):
  template_name = "htmx/purchase_item_modal.html"
  base_template = "full_modal.html"

  def get(self, request, *args, **kwargs):
    menu_item = models.MenuItem.objects.get(pk=self.kwargs.get(self.pk_url_kwarg))
    self.extra_context = {'current_menu_item': menu_item, 'basetemplate': self.base_template}
    return super().get(self, request, *args, **kwargs)
  
  # def post(self, request, *args, **kwargs):
  #   return super().post(self, request, *args, **kwargs)
  
  # def post(self, request, *args, **kwargs):
  #   return super().post(self, request, *args, **kwargs)
    # response = HttpResponse()
    # response['Hx-Redirect'] = "/purchases"
    # return response

# Update Views

class UpdateIngredient(LoginRequiredMixin, UpdateView):
  template_name = "inventory/update_ingredient.html"
  model = models.Ingredient
  form_class = forms.IngredientForm
  extra_context = {'active_nav_pantry': "active"}

class HtmxUpdateIngredient(UpdateIngredient):
  template_name = 'htmx/update_ingredient.html'
  
  def get_success_url(self):
    return reverse('htmx_ingredient', args=(self.object.pk,))

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

class HtmxUpdateRecipeRequirement(UpdateRecipeRequirement):
  template_name = "htmx/update_recipe_req.html"

  def get_success_url(self):
    return reverse('htmx_recipe_req', args=(self.object.pk,))

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

class HtmxDeleteIngredient(DeleteIngredient):
  template_name = "htmx/delete_ingredient_modal.html"
  extra_context = {'basetemplate': 'full_modal.html'}

  def get_success_url(self):
    return "/ingredients"

  def delete(self, request, *args, **kwargs):
    self.object = self.get_object()
    # response = HttpResponse()
    # response['HX-Redirect'] = self.get_success_url()
    self.object.delete()
    return render(request, "htmx/delete_table_row.html", {'columns': 4, 'thing': 'Ingredient'})

class DeleteMenuItem(LoginRequiredMixin, DeleteView):
  template_name = "inventory/delete_menu_item.html"
  model = models.MenuItem
  success_url = "/menu"
  extra_context = {'active_nav_menu': "active"}

class HtmxDeleteMenuItem(DeleteMenuItem):
  template_name = "htmx/delete_menu_item_modal.html"
  extra_context = {'basetemplate': 'full_modal.html'}

  def delete(self, request, *args, **kwargs):
    self.object = self.get_object()
    response = HttpResponse()
    response['HX-Redirect'] = self.get_success_url()
    self.object.delete()
    return response

class DeleteRecipeRequirement(LoginRequiredMixin, DeleteView):
  template_name = "inventory/delete_recipe_req.html"
  model = models.RecipeRequirement
  success_url = "/recipes"
  extra_context = {'active_nav_recipes': "active"}

@method_decorator(csrf_exempt, name='dispatch')
class HtmxDeleteRecipeRequirement(DeleteRecipeRequirement):
  def delete(self, request, *args, **kwargs):
    super().delete(self, request, *args, **kwargs)
    # self.object = self.get_object()
    # self.object.delete()
    return render(request, 'htmx/delete_table_row.html', {'columns': 3, 'thing': 'Recipe requirement'})

@method_decorator(csrf_exempt, name='dispatch')
class DeletePurchase(DeleteView):
  template_name = "inventory/delete_purchase.html"
  model = models.Purchase
  success_url = "/purchases"
  extra_context = {'active_nav_purchases': "active"}

  def delete(self, request, *args, **kwargs):
    if request.htmx:
      super().delete(self, request, *args, **kwargs)
      return render(request, 'htmx/delete_table_row.html', {'columns': 4, 'thing': 'Order'})
    else:
      return super().delete(self, request, *args, **kwargs)