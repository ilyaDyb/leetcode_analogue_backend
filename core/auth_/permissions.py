from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed

from rest_framework_simplejwt.tokens import AccessToken

from core.auth_.models import User

class CustomIsAuthenticatedPermission(BasePermission):
    def has_permission(self, request, view):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return False

        try:
            token_str = auth_header.split()[1]
            token = AccessToken(token_str)
            user_id = token["user_id"]
            user_instance = User.objects.get(pk=user_id)
        except Exception:
            raise AuthenticationFailed({"detail": "Invalid token or user not found"})

        if user_instance.is_authenticated:
            request.user = user_instance
            return True
        return False
    
class CustomIsAdminPermission(CustomIsAuthenticatedPermission):
    def has_permission(self, request, view):
        has_permission = super().has_permission(request, view)
        if has_permission and request.user.is_staff:
            return True
        return False
