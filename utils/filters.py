from rest_framework.filters import BaseFilterBackend
from temporal_owner.models import TemporalOwner


class IsOwnerFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        user = request.user
        if user.is_authenticated and isinstance(user, TemporalOwner) and not user.is_superuser:
            return queryset.filter(owner=request.user.id)
        return queryset