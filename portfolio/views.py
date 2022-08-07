from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render

from .serializers import ProjectSerializer
from .models import Project, Technologies
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Create your views here.


class ProjectsView(APIView):
    def get(self, request:HttpRequest) -> Response:
        queryset = Project.objects.all()
        serializer = ProjectSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProjectDetailView(APIView):
    def get(self, request:HttpRequest, pk:int) -> Response:
        project = get_object_or_404(Project, pk=pk)
        serializer = ProjectSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)