from django.shortcuts import render
from .models import Project
from .serializers import ProjectSerializer
# Create your views here.
from rest_framework import viewsets

class ProjectViewSet(viewsets.ModelViewSet):
    """
    This viewset should automatically provide `list` `create`, `update`
    `destroy` and `retrieve` actions.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

