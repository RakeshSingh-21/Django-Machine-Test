from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Client, Project

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
        
class ProjectSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'project_name', 'client', 'users', 'created_at', 'created_by']
    
    def validate_users(self, value):
        # Ensure that the users field contains a list of valid user IDs
        if not all(isinstance(user_id, int) for user_id in value):
            raise serializers.ValidationError("User IDs must be integers.")
        return value
    
class ClientSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'client_name', 'projects','users', 'created_at', 'created_by', 'updated_at']
        