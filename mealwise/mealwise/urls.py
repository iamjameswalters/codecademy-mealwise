"""mealwise URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from inventory import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('robots.txt', views.Robots.as_view(), name="robots"),
    path("accounts/", include("django.contrib.auth.urls")),
    path('signup/', views.CreateAccount.as_view(), name="signup"),
    path('', views.HomeView.as_view(), name="home"),
    path('menu/', views.Menu.as_view(), name="menu"),
    path('recipes/', views.RecipeRequirements.as_view(), name="recipes"),
    path('ingredients/', views.Ingredients.as_view(), name="ingredients"),
    path('purchases/', views.Purchases.as_view(), name="purchases"),
    path('report/', views.ReportView.as_view(), name="report"),
    path("ingredients/add", views.CreateIngredient.as_view(), name="create_ingredient"),
    path("menu/add", views.CreateMenuItem.as_view(), name="create_menu_item"),
    path("recipes/add", views.CreateRecipeRequirement.as_view(), name="create_recipe_req"),
    path("purchases/add", views.CreatePurchase.as_view(), name="create_purchase"),
    path('ingredients/<pk>/', views.UpdateIngredient.as_view(), name="update_ingredient"),
    path('menu/<pk>/', views.UpdateMenuItem.as_view(), name="update_menu_item"),
    path('recipes/<pk>/', views.UpdateRecipeRequirement.as_view(), name="update_recipe_req"),
    path('purchases/<pk>/', views.UpdatePurchase.as_view(), name="update_purchase"),
    path('ingredients/<pk>/remove', views.DeleteIngredient.as_view(), name="delete_ingredient"),
    path('menu/<pk>/remove', views.DeleteMenuItem.as_view(), name="delete_menu_item"),
    path('recipes/<pk>/remove', views.DeleteRecipeRequirement.as_view(), name="delete_recipe_req"),
    path('purchases/<pk>/remove', views.DeletePurchase.as_view(), name="delete_purchase"),
]
