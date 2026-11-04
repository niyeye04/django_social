from django.shortcuts import render,get_object_or_404
from rest_framework import views,parsers,status,generics,permissions,authentication
from rest_framework.response import Response
from . import user_serializers
from groups.models import Group
from users.models import CustomUser as User
# Create your views here.
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

#User Views
    
class UserRegisteringView(generics.CreateAPIView):
    serializer_class = user_serializers.UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = [parsers.FormParser,parsers.MultiPartParser]
    #authentication_classes = [authentication.TokenAuthentication]




class ProfileUpdateView(views.APIView):
    serializer_class = user_serializers.ProfileUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.JSONParser,parsers.FormParser, parsers.MultiPartParser]
    authentication_classes = [authentication.SessionAuthentication,authentication.TokenAuthentication]

    def put(self,request,*args, **kwargs):
        serializer = self.serializer_class(instance=request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
    def patch(self,request,*args, **kwargs):
        serializer = self.serializer_class(instance = request.user,data = request.data,partial = True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

class JoinGroupView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]

    def get(self,request,group_id,*args, **kwargs):
        group = get_object_or_404(Group,id = group_id)
        group.members.add(request.user)
        return Response({"message" : "Joined the group successfully"}, status=status.HTTP_202_ACCEPTED)
    

class LeaveGroupView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]

    def get(self,request,group_id,*args, **kwargs):
        group = get_object_or_404(Group,id = group_id)
        user = request.user
        if user in group.admin.all() and user in group.members.all():
            group.members.remove(user)
            group.admin.remove(user)
            return Response({"message" : "Left the group successfully"}, status=status.HTTP_202_ACCEPTED)
        elif user in group.members.all():
            group.members.remove(user)
            return Response({"message" : "Left the group successfully"}, status=status.HTTP_202_ACCEPTED)
        
        return Response({"message" : "User not in this group"}, status=status.HTTP_404_NOT_FOUND)


class FollowAndUnFollowingViews(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]

    def get(self, request,following, user_being_followed_id,*args, **kwargs):
        user = request.user
        user_being_followed = get_object_or_404(User, id = user_being_followed_id)
        if user_being_followed.id == user.id:
            return Response({"message":"Sorry Can't follow or unfollow yourself"})
        else:
            if following:
                if user in user_being_followed.followers.all():
                    return Response({"message":"followed succssefully"})
                else:
                    user_being_followed.followers.add(user)
                    return Response({"message":"followed succssefully"})
            else:
                if user in user_being_followed.followers.all():
                    user_being_followed.followers.remove(user)
                    return Response({"message":"Unfollowed succssefully"})

                else:
                    return Response({"message":"Unfollowed succssefully"})


class ListUserView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = user_serializers.ListUserSerializers
    authentication_classes = [authentication.SessionAuthentication,authentication.TokenAuthentication]
    

class SignUpView(views.APIView):
    permission_classes = [permissions.AllowAny]
    