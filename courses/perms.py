from rest_framework import permissions


class IsTeacher(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.userRole.name.lower() == 'teacher'


class IsStudent(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.userRole.name.lower() == 'student'


class IsAdmin(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.userRole.name.lower() == 'admin'


class IsTeacherOrAdmin(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request,
                                      view) and (request.user.userRole.name.lower() == 'teacher' or request.user.userRole.name.lower() == 'admin')
