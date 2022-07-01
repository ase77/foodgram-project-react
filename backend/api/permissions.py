from rest_framework import permissions

# class RetrievePermission(permissions.BasePermission):

#     def has_permission(self, request, view):
#         if view.action == 'retrieve':
#             return request.user.is_authenticated()
#         return True

#     def has_object_permission(self, request, view, obj):
#         if not request.user.is_authenticated():
#             return False
#         return True
