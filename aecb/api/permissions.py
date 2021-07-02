from rest_framework import permissions
from .auth import GoogleTokenAuth


class ClientPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        token = request.headers.get("Token", "")
        auth_result = GoogleTokenAuth.authenticate(token)
        self.message = auth_result.detail if auth_result.account is None else "This operation is exclusive for client role. {detail}.".format(
            detail=auth_result.detail)

        return False if auth_result.account is None else auth_result.account.role == "client"


class AdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        token = request.headers.get("Token", "")
        auth_result = GoogleTokenAuth.authenticate(token)
        self.message = auth_result.detail if auth_result.account is None else "This operation is exclusive for admin role. {detail}.".format(
            detail=auth_result.detail)

        return False if auth_result.account is None else auth_result.account.role == "admin"
