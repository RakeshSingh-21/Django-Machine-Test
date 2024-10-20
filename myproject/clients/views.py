from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Client, Project, User
from .Serializers import ClientSerializer, ProjectSerializer
from django.shortcuts import get_object_or_404

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
        


    def update(self, request, *args, **kargs):
        client = self.get_object()
        client.client_name = request.data.get("client_name", client.client_name)
        client.save()
        return Response(ClientSerializer(client).data)
    
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)  # If it's a PATCH request, set partial to True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        #Get the object (client) to be updated
        client = self.get_object()

        # Use the serializer's 'partial=True' flag to allow partial updates
        serializer = self.get_serializer(client, data=request.data, partial=True)

        # ensure data is valid
        serializer.is_valid(raise_exception=True)

        # Save the updated client object
        serializer.save()

        # Return the updated data in response
        return Response(serializer.data)


    def destroy(self, request, *args, **kwargs):
        # instance = self.get_object()
        # self.perform_destroy(instance)
        super().destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    # Override create method for project creation
    def create(self, request, client_id=None):
        client = get_object_or_404(Client, pk=client_id)
        project_name = request.data.get("project_name")
        users_data = request.data.get("users", [])

        # Create project
        project = Project.objects.create(project_name=project_name, client=client, created_by=request.user)

        # Assign users to project
        user_ids = [user['id'] for user in users_data]
        users = User.objects.filter(id__in=user_ids)
        project.users.set(users)
        project.save()


        return Response(ProjectSerializer(project).data, status=status.HTTP_201_CREATED)

    # List projects assigned to the logged-in user
    def list(self, request):
        # Get all projects where the user is assigned
        user_projects = request.user.assigned_projects.all()

        # Serialize the data
        serializer = ProjectSerializer(user_projects, many=True)

        # Return the response
        return Response(serializer.data)