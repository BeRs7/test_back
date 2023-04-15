from django.utils.translation import gettext_lazy as _

from rest_framework.permissions import BasePermission


class OnlyUnauthorized(BasePermission):
    """
    Allows access only to unauthorized users.
    """

    def has_permission(self, request, view):
        return request.user.is_anonymous


class OnlyAuthorized(BasePermission):
    """
    Allows access only to unauthorized users.
    """

    message = _("Требуется авторизация")

    def has_permission(self, request, view):
        return request.user.is_authenticated
