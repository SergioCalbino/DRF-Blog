from rest_framework.permissions import BasePermission

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        else:
            return request.is_staff


from rest_framework.permissions import BasePermission

from rest_framework.permissions import BasePermission

class IsOwnerOrStaff(BasePermission):
    def has_permission(self, request, view):
        # Permitir solo lectura para métodos GET, HEAD, OPTIONS
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        # Permitir escritura (crear comentario) solo a usuarios autenticados
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Permitir la edición y eliminación solo si el usuario es el propietario del comentario o un usuario de staff
        if request.method in ['PUT', 'DELETE']:
            return obj.user == request.user or request.user.is_staff  # Verificar que el usuario sea propietario o staff
        return True  # Para GET, HEAD y OPTIONS, no hay restricción

