from django.shortcuts import render
from rest_framework import views,parsers,status,generics,permissions,authentication
from rest_framework.response import Response
from . import post_serializers
from posts.models import Post
from django.shortcuts import get_object_or_404
# Create your views here.


class createPostView(views.APIView):
    #queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.FormParser, parsers.MultiPartParser]
    authentication_classes = [authentication.SessionAuthentication,authentication.TokenAuthentication]

    def post(self,request):
        serializer = post_serializers.CreatePostSerializer(request.user, data = request.data)
        if serializer.is_valid():
            serializer.save(owner = request.user)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    

        
class createPostView2(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.FormParser, parsers.MultiPartParser]
    authentication_classes = [authentication.SessionAuthentication,authentication.TokenAuthentication]
    serializer_class = post_serializers.CreatePostSerializer


class DeletePostView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.FormParser, parsers.MultiPartParser]
    authentication_classes = [authentication.SessionAuthentication,authentication.TokenAuthentication]
    serializer_class = post_serializers.DeletePostSerializer
    
    def delete(self,request,post_id,*args, **kwargs):
        #get the post instance
        post = get_object_or_404(Post, id = post_id, owner = request.user)
        post.delete()
        Response({"message": "POst deleted successfull"}, status = status.HTTP_204_NO_CONTENT)

class UpdatePostView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.FormParser, parsers.MultiPartParser]
    authentication_classes = [authentication.SessionAuthentication,authentication.TokenAuthentication]
    serializer_class = post_serializers.UpdatePostSerializer

    
    def put(self,request,post_id,*args, **kwargs):
        post = get_object_or_404(Post,id = post_id,owner = request.user)
        serializer = self.serializer_class(instance = post, partial = True, data = request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def patch(self,request,post_id,*args, **kwargs):
        post = get_object_or_404(Post,id = post_id,owner = request.user)
        serializer = self.serializer_class(instance = post, partial = True, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    