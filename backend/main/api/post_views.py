from django.shortcuts import render
from rest_framework import views,parsers,status,generics,permissions,authentication
from rest_framework.response import Response
from . import post_serializers
from posts.models import Post
from django.shortcuts import get_object_or_404
# Create your views here.


# class createPostView(views.APIView):
#     #queryset = Post.objects.all()
#     permission_classes = [permissions.IsAuthenticated]
#     parser_classes = [parsers.FormParser, parsers.MultiPartParser]
#     authentication_classes = [authentication.SessionAuthentication,authentication.TokenAuthentication]
    
#     def get_serializer_class(self):
#         if self.request.data.get('group') is None:
#             return post_serializers.CreateIndividualPostSerializer
#         post_serializers.CreateGroupPostSerializer

#     def post(self,request):
#         serializer_class = self.get_serializer_class()
#         serializer = serializer_class(data = request.data, context = {'request': request})
#         if serializer.is_valid():
#             serializer.save(owner = request.user)
#             return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
#         return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    

        
class createPostView2(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.FormParser, parsers.MultiPartParser]
    authentication_classes = [authentication.SessionAuthentication,authentication.TokenAuthentication]
    #serializer_class = post_serializers.CreatePostSerializer
    queryset = Post.objects.all()


    # def get_serializer_class(self):
    #     if self.request.data.get('group') is None:
    #         return post_serializers.CreateIndividualPostSerializer  # Use individual serializer
    #     return post_serializers.CreateGroupPostSerializer  # Use group serializer

    def get_serializer_class(self):
        return post_serializers.CreateGroupPostSerializer  # Use individual serializer
            


    def create(self,request,*args, **kwargs):
        group = request.data.get('group')
        
        if group is None:
            serializer_class = post_serializers.CreateIndividualPostSerializer
        else:
            serializer_class = post_serializers.CreateGroupPostSerializer

        serializer = serializer_class(data = request.data, context = {'request': request})

        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"mesage":"Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)

        


class DeletePostView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.FormParser, parsers.MultiPartParser]
    authentication_classes = [authentication.SessionAuthentication,authentication.TokenAuthentication]
    serializer_class = post_serializers.DeletePostSerializer
    
    def delete(self,request,post_id,*args, **kwargs):
        #get the post instance
        post = get_object_or_404(Post, id = post_id, owner = request.user)
        post.delete()
        Response({"message": "Post deleted successfull"}, status = status.HTTP_204_NO_CONTENT)



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
    

    
class ListPostView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = post_serializers.ReturnPostSerializer
    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]