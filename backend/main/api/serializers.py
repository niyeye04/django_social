from rest_framework import serializers
from users.models import User

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["profile_pic","phonenumber","birthdate","bio"]