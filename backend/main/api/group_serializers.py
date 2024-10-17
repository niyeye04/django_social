from rest_framework import serializers,validators
from django.contrib.auth.password_validation import validate_password
from users.models import CustomUser
from groups.models import Group


class ListGroupSerializer(serializers.ModelSerializer):
    time_since_created = serializers.DateTimeField(read_only = True)

    class Meta:
        model = Group
        fields = ["id",'name','description', "profile_pic", 'time_since_created',"admin","members"]

class CreateGroupSerializer(serializers.ModelSerializer):
    #admin = serializers.ReadOnlyField(read_only = True)
    class Meta:
        model = Group
        fields = ['name','description', "profile_pic"]


        def create(self,validated_data):
            group = Group.objects.create(**validated_data)
            group.save()
            return group

class DeleteGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

class UpdateGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        exclude = ['created_at','posts','admin','members']
        