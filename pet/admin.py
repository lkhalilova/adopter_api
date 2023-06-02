from django.contrib import admin
from .models import Pet


@admin.action(description="Make all selected pets older by 1 year or month")
def make_older(modeladmin, request, queryset):
    for pet in queryset:
        pet.age += 1
        pet.save()


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'species', 'age', 'gender', 'city')
    list_filter = ('species', 'city')
    search_fields = ('name', 'species', 'city')
    actions = [make_older]



