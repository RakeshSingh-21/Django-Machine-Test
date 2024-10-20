from django.contrib.auth.models import User
from django.db import models

class Client(models.Model):
    client_name = models.CharField(max_length=255)
    created_by =  models.ForeignKey(User, related_name='created_clients', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.client_name
    

class Project(models.Model):
    project_name = models.CharField(max_length=255)
    client = models.ForeignKey(Client, related_name='projects', on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name='assigned_projects')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='created_projects', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.project_name