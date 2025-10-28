from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

Profile = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = Profile
        fields = ['username', 'email', 'password', 'profile_picture', 'bio',]

    def create(self, validated_data):
        user = Profile(
            username = validated_data['username'],
            email = validated_data['email'],
            profile_picture = validated_data.get('profile_picture', None),
            bio = validated_data.get('bio', ''),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user 
    

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError("Invalid credentials.")
        else:
            raise serializers.ValidationError("Both username and password are required.")
        data['user'] = user
        return data
    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['username', 'email', 'profile_picture', 'bio',]


