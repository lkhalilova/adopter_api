from rest_framework.permissions import BasePermission
from temporal_owner.models import TemporalOwner


class IsCustomAdminUser(BasePermission):
    """
    Checks if user is TemporalOwner object (is_admin=True.)
    """

    def has_permission(self, request, view):
        user = request.user
        return isinstance(user, TemporalOwner) and user.is_admin