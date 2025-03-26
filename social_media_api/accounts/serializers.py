from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        firleds = ['id', 'username', 'email', 'bio', 'profile_picture', 'followers']

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password', 'bio', 'profile_picture']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = get_user_model().objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'],)
        user.bio = validated_data.get('bio', '')
        user.profile_picture = validated_data.get('profile_picture', '')
        user.save()
        return user
    
class TokenSerializer(serializers.ModelSerializer):
    token = serializers.CharField()

    class Meta:
        model = Token
        fields = ['token']

    def create(self, validated_data):
        user = validated_data.get("user")
        token,created = Token.objects.get_or_create(user=user)
        return token
                                  

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)