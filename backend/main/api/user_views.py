from django.shortcuts import render,get_object_or_404
from rest_framework import views,parsers,status,generics,permissions,authentication
from rest_framework.response import Response
from . import user_serializers
from groups.models import Group
# Create your views here.

#User Views
    
class UserRegisteringView(generics.CreateAPIView):
    serializer_class = user_serializers.UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = [parsers.FormParser,parsers.MultiPartParser]
    #authentication_classes = [authentication.TokenAuthentication]


class ProfileUpdateView(views.APIView):
    serializer_class = user_serializers.ProfileUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.FormParser,parsers.MultiPartParser]
    authentication_classes = [authentication.SessionAuthentication,authentication.TokenAuthentication]

    def put(self,request,*args, **kwargs):
        serializer = self.serializer_class(instance = request.user,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
    def patch(self,request,*args, **kwargs):
        serializer = self.serializer_class(instance = request.user,data = request.data,partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

class JoinGroupView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]

    def get(self,request,group_id,*args, **kwargs):
        group = get_object_or_404(Group,id = group_id)
        group = group.save()
        group.members.add(request.user)
        return Response("{message : Joined the group successfully}", status=status.HTTP_202_ACCEPTED)



