from rest_framework.permissions import BasePermission
from .models import Company


class IsAdminUser(BasePermission):
    """
    Custom permission to only allow access to users associated with a Company
    that has an ADMIN role. Does NOT use is_staff or is_superuser.
    """
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            hasattr(request.user, 'company') and
            request.user.company.role == Company.Role.ADMIN
        )
