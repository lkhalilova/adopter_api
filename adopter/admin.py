from django.contrib import admin
from .models import Adopter
from adoption_request.models import AdoptionRequest


class AdoptionRequestInline(admin.TabularInline):
    model = AdoptionRequest


@admin.register(Adopter)
class AdopterAdmin(admin.ModelAdmin):
    inlines = [
        AdoptionRequestInline,
    ]