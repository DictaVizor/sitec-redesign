from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    message = 'Solo el propietario puede modificar esta informacion'

    def has_object_permission(self, request, view, obj):
        return obj.owner == self.request.user