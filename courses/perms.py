from rest_framework import permissions


class IsTeacher(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.user_role.name.lower() == 'teacher'


class IsStudent(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.user_role.name.lower() == 'student'


class IsAdmin(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.user_role.name.lower() == 'admin'


class IsTeacherOrAdmin(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request,
                                      view) and (request.user.user_role.name.lower() == 'teacher' or request.user.user_role.name.lower() == 'admin')
