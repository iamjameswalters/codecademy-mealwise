from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Ingredient)
admin.site.register(models.MenuItem)
admin.site.register(models.RecipeRequirement)
admin.site.register(models.Purchase)