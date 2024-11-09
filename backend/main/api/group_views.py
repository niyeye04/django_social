from django.shortcuts import render
from rest_framework import views,parsers,status,generics,permissions,authentication
from rest_framework.response import Response
from . import group_serializers
from users.models import CustomUser as User
from groups.models import Group
from django.shortcuts import get_object_or_404
from . import permissionfile

class CreateGroupView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.FormParser, parsers.MultiPartParser]
    serializer_class = group_serializers.CreateGroupSerializer

    def perform_create(self, serializer):
        group = serializer.save()
        group.admin.add(self.request.user)
        group.members.add(self.request.user)
        

class DeleteGroupView(views.APIView):
    permission_classes = [permissions.IsAuthenticated, permissionfile.IsGroupAdmin,permissions.DjangoModelPermissions]
    #parser_classes = [parsers.FormParser, parsers.MultiPartParser]
    serializer_class = group_serializers.DeleteGroupSerializer

    def delete(self,request,group_id,*args, **kwargs):
        group = get_object_or_404(Group, id = group_id,)

        if group.delete():
            return Response({"message": "Group  deleted successfull"}, status = status.HTTP_204_NO_CONTENT)
        return Response({"message": "Group not deleted successfull"}, status = status.HTTP_400_BAD_REQUEST)
    


class UpdateGroupView(views.APIView):
    permission_classes = [permissions.IsAuthenticated,permissionfile.IsGroupAdmin, ]
    parser_classes = [parsers.FormParser, parsers.MultiPartParser]
    serializer_class = group_serializers.UpdateGroupSerializer
    queryset = Group.objects.all()
    

    def put(self,request,group_id,*args, **kwargs):
        group = get_object_or_404(Group,id = group_id)
        self.check_object_permissions(request, group)
        serializer = self.serializer_class(instance = group,data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST) 
    
    def patch(self,request,group_id,*args, **kwargs):
        group = get_object_or_404(Group,id = group_id,)
        self.check_object_permissions(request,group)
        serializer = self.serializer_class(instance = group, data = request.data, partial = True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
class ListGroupsView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.FormParser, parsers.MultiPartParser]
    serializer_class = group_serializers.ListGroupSerializer
    queryset = Group.objects.all()

class AddGroupMembersView(views.APIView):
    permission_classes = [permissionfile.IsGroupAdmin]
    serializer_class = group_serializers.UpdateGroupSerializer
 

    def get(self,request,group_id,user_id,*args, **kwargs):
        group = get_object_or_404(Group, id = group_id)
        user = get_object_or_404(User, id = user_id)
        self.check_object_permissions(request,group)
        group.members.add(user)
        return Response({"message": "User added successfull"}, status = status.HTTP_201_CREATED)

    

class AddGroupAdminView(views.APIView):
    permission_classes = [permissionfile.IsGroupAdmin]
    serializer_class = group_serializers.UpdateGroupSerializer
 
    def get(self,request,group_id,user_id,*args, **kwargs):
        group = get_object_or_404(Group, id = group_id)
        user = get_object_or_404(User, id = user_id)
        self.check_object_permissions(request,group)

        if user in group.admin.all():
            return Response ({"message": "User is already an admin in this group"})
        
        elif user not in group.members.all():
            group.members.add(user)

        group.admin.add(user)

        return Response({"message": "Admin added successfull"}, status = status.HTTP_201_CREATED)
    

class RemoveGroupAdminView(views.APIView):
    permission_classes = [permissionfile.IsGroupAdmin]
    serializer_class = group_serializers.UpdateGroupSerializer
    
    def get(self,request,group_id,user_id,*args, **kwargs):
        group = get_object_or_404(Group, id = group_id)
        user = get_object_or_404(User, id = user_id)
        self.check_object_permissions(request,group)

        if user in group.admin.all():
            group.admin.remove(user)
            return Response({"message": "Admin removed successfull"}, status = status.HTTP_201_CREATED)
        
        elif user not in group.admin.all():
            return Response({"message": "User is not an admin in this group"}, status = status.HTTP_201_CREATED)



class RemoveGroupMemberView(views.APIView):
    permission_classes = [permissionfile.IsGroupAdmin]
    serializer_class = group_serializers.UpdateGroupSerializer
    
    def get(self,request,group_id,user_id,*args, **kwargs):
        group = get_object_or_404(Group, id = group_id)
        user = get_object_or_404(User, id = user_id)
        self.check_object_permissions(request,group)

        if user in group.members.all():
            group.members.remove(user)
            return Response({"message": "Member removed successfull"}, status = status.HTTP_201_CREATED)
        
        elif user not in group.members.all():
            return Response({"message": "User is not a member in this group"}, status = status.HTTP_201_CREATED)