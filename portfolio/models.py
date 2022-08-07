from django.db import models
# Create your models here.

class Technologies(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ImageField(upload_to='icons', null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Project(models.Model):
    name = models.CharField(max_length=255)
    link = models.URLField()
    path = models.CharField(max_length=255, unique=True)
    video = models.URLField()
    image = models.ImageField(upload_to='images/', blank=True)
    github = models.URLField()
    description = models.TextField()
    technologies = models.ManyToManyField(Technologies)
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name