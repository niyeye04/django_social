from rest_framework import permissions
from groups.models import Group

#permission to check if the user is an admin in a respective group
class IsGroupAdmin(permissions.BasePermission):
    message = "Sorry,only the admin can perform this task"
    def has_permission(self, request, view):
        return request.user.is_authenticated
            
    
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Group):
            return request.user in obj.admin.all()
        return False
    
    

