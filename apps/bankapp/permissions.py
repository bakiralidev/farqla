# permissions.py
from rest_framework.permissions import BasePermission

class IsCustomAdmin(BasePermission):
    """is_admin=True bo‘lgan userlar uchun."""
    message = "Faqat admin foydalanuvchilar kirishi mumkin."

    def has_permission(self, request, view):
        user = getattr(request, "user", None)
        return bool(user and user.is_authenticated and getattr(user, "is_admin", False))


class IsOwnerOrAdmin(BasePermission):
    """
    Admin bo‘lsa — ruxsat.
    Admin bo‘lmasa — obj.user/created_by/owner dan biri request.user bo‘lsa ruxsat.
    """
    message = "Sizda bu resursni ko‘rish huquqi yo‘q."

    def has_object_permission(self, request, view, obj):
        user = getattr(request, "user", None)
        if not (user and user.is_authenticated):
            return False
        if getattr(user, "is_admin", False):
            return True
        for attr in ("user", "created_by", "owner"):
            if getattr(obj, attr, None) == user:
                return True
        return False
