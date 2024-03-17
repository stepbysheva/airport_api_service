from rest_framework.permissions import BasePermission, SAFE_METHODS


class IFADMINORREADONLY(BasePermission):
    def has_permission(self, request, view):
        return ((request.user.is_authenticated and request.method in SAFE_METHODS)
                or (request.user.is_authenticated and request.user.is_staff))
