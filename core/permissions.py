from rest_framework import permissions


class MyUserPermission(permissions.BasePermission):

    def has_permission(self, request, view):

        if view.action in ['list', 'activity', 'retrieve']:
            return request.user.is_superuser
        return False
