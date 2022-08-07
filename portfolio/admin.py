from django.contrib import admin
from .models import Project, Technologies
# Register your models here.

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'github')
    list_filter = ('name', 'date_added', 'last_updated', 'technologies')
    search_fields = ('name',)


@admin.register(Technologies)
class TechnologiesAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name', 'date_added', 'last_updated')
    search_fields = ('name',)