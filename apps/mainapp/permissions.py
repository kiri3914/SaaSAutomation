from rest_framework import permissions


class CourseAndMentorPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if request.user.is_staff:
            return request.user.branch == obj.branch

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return False

