from django.shortcuts import render
from rest_framework import views,parsers,status,generics,permissions,authentication
from rest_framework.response import Response
from . import serializers
# Create your views here.

#User Views
    
class UserRegisteringView(generics.CreateAPIView):
    serializer_class = serializers.UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = [parsers.FormParser,parsers.MultiPartParser]
    #authentication_classes = [authentication.TokenAuthentication]


class ProfileUpdateView(views.APIView):
    serializer_class = serializers.ProfileUpdateSerializer
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


#Group Views