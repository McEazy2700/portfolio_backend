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
    name = models.CharField(max_length=255, null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    path = models.CharField(max_length=255, unique=True, null=True, blank=True)
    video = models.URLField(null=True, blank=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    github = models.URLField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    technologies = models.ManyToManyField(Technologies)
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-date_added']