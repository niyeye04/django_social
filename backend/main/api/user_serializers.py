from rest_framework import serializers,validators
from django.contrib.auth.password_validation import validate_password
from users.models import CustomUser
from posts.models import Post
        
#User Serializers
class UserRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required = True, validators = [validators.UniqueValidator(queryset = CustomUser.objects.all())])
    email = serializers.CharField(required = True, validators = [validators.UniqueValidator(queryset= CustomUser.objects.all())])
    password = serializers.CharField(write_only = True, required = True, validators = [validate_password])
    password2 = serializers.CharField(write_only = True, required = True)

    class Meta:
        model = CustomUser
        fields = ['profile_pic','username','email','password','password2']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("The password field don't match")
        return data
        
    def create(self, validated_data):
        user =  CustomUser.objects.create(
            profile_pic = validated_data["profile_pic"],
            username = validated_data["username"],
            email = validated_data["email"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return user
    

class ProfileUpdateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required = False,validators = [validators.UniqueValidator(queryset=CustomUser.objects.all())])
    class Meta:
        model = CustomUser
        fields = ["email","profile_pic","phone_number","birthdate","bio"]


