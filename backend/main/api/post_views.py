from django.shortcuts import render
from rest_framework import views,parsers,status,generics,permissions,authentication
from rest_framework.response import Response
from . import post_serializers
from posts.models import Post,Comments
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
        return post_serializers.CreateGroupPostSerializer  # Use Group serializer
            


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



class WriteCommentView(generics.CreateAPIView):
    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]
    queryset = Comments.objects.all()
    serializer_class = post_serializers.WriteCommentSerializer

    # def get_serializer_context(self):
    #     context = super().get_serializer_context()
    #     context['request'] = self.request  # Adding the request to the context
    #     return context
        

    def create(self,request,*args, **kwargs):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)

        #copy the data from the actual request
        data = request.data.copy()
        # data['owner'] = request.user.id
        # data['post'] = post_id


        serializer = self.serializer_class(data = data, context={'request': request})  
        if serializer.is_valid(raise_exception=True):
            serializer.save(owner = request.user, post = post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        return Response({"message":"Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)
    

class LikeAndDislikeView(views.APIView):
    authentication_classes = [authentication.SessionAuthentication,authentication.TokenAuthentication]

    def get(self,request,post_id,like_post,*args, **kwargs):
        post = get_object_or_404(Post,id = post_id)

        if like_post:
            if request.user in post.likes.all():
                return Response({"mesage":"Liked succussfully"})
            elif request.user not in post.likes.all():
                if request.user in post.dislikes.all():
                    post.dislikes.remove(request.user)
                post.likes.add(request.user)
                return Response({"mesage":"Liked succussfully"})
        
        else:
            if request.user in post.dislikes.all():
                return Response({"mesage":"Disliked succussfully"})
            
            elif request.user not in post.dislikes.all():
                if request.user in post.likes.all():
                    post.likes.remove(request.user)
                post.dislikes.add(request.user)
                return Response({"mesage":"Disliked succussfully"})
                