from rest_framework import serializers,validators
from django.contrib.auth.password_validation import validate_password
from users.models import CustomUser
from posts.models import Post


#Posts Selializers
class CreateIndividualPostSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Post
        fields = ['owner','content','caption']

    def create(self,validated_data):
        request = self.context.get('request')
        validated_data['owner'] = request.user
        post = Post.objects.create(**validated_data)
        return post

class CreateGroupPostSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Post
        fields = ['owner','group','content','caption']

    def create(self,validated_data):
        request = self.context.get('request')
        validated_data['owner'] = request.user
        post = Post.objects.create(**validated_data)
        return post
    


        
class ReturnPostSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only = True)
    time_since_posted = serializers.ReadOnlyField()
    is_group_post = serializers.ReadOnlyField()
    class Meta:
        model =  Post
        fields = ['owner','is_group_post','content','caption','created_at',"likes","dislikes","time_since_posted"]


class DeletePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class UpdatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id','owner','content', 'caption']
        read_only_fields = ['id','owner']

    def update(self,instance,validates_data):
        instance.content = validates_data.get('content', instance.content)
        instance.caption = validates_data.get('content', instance.caption)
        instance.save()
        return instance