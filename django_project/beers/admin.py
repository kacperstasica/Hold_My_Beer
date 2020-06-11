from django.contrib import admin

from beers.models import Beer


@admin.register(Beer)
class BeerModelAdmin(admin.ModelAdmin):
    pass
