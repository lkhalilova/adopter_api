from django.contrib import admin
from .models import TemporalOwner
from pet.models import Pet


class PetInline(admin.TabularInline):
    model = Pet


@admin.register(TemporalOwner)
class TemporalOwnerAdmin(admin.ModelAdmin):
    inlines = [
        PetInline,
    ]
    list_display = ('first_name', 'last_name', 'city', 'is_admin', 'is_superuser', 'is_staff')
    list_filter = ('city', 'is_admin', 'is_superuser')
    search_fields = ('first_name', 'last_name', 'city', 'username')
    empty_value_display = "-empty-"

    fieldsets = [
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'city')}),
        ('Permissions', {'fields': ('is_admin', 'is_superuser', 'is_staff')}),
    ]

    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["username", "first_name", "last_name", 'city', "password"],
            },
        ),
    ]

    ordering = ["username"]
    filter_horizontal = []