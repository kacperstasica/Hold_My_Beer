from django.contrib import admin

from beers.models import Beer, Review


@admin.register(Beer)
class BeerModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Review)
class ReviewModelAdmin(admin.ModelAdmin):
    fields = [
        'content',
        'author',
        'beer'
    ]
