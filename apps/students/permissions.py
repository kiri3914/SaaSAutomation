from rest_framework import permissions


class StudentPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return True
            return request.user.branch == obj.course.branch

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return True
        return False


class PaymentsPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return True
            return request.user.branch == obj.student.course.branch

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return True
        return False
