from rest_framework import serializers
from .models import Project, Technologies

class TechnologiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Technologies
        fields = ['name', 'id']

class ProjectSerializer(serializers.ModelSerializer):
    technologies = TechnologiesSerializer(many=True)
    class Meta:
        model = Project
        fields = ['id', 'name', 'link', 'path', 'video', 'image', 'github', 'description', 'technologies']