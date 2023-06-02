from django.contrib import admin
from .models import AdoptionRequest


@admin.action(description="approve all selected requests")
def approve(modeladmin, request, queryset):
    for adoption_request in queryset:
        adoption_request.approved = True
        adoption_request.save()


@admin.register(AdoptionRequest)
class AdoptionRequestAdmin(admin.ModelAdmin):
    list_display = ('pet', 'adopter', 'approved', 'created_at')
    list_filter = ('approved',)
    search_fields = ('pet__name', 'adopter__first_name', 'adopter__last_name', 'adopter__city')
    date_hierarchy = "created_at"
    actions = [approve]


