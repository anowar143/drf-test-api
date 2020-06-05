from rest_framework.permissions import BasePermission


class UserIsOwnerApp(BasePermission):

    def has_object_permission(self, request, view, app):
        return request.user.id == app.user.id
