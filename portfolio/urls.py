from django.urls import path
from . import views


urlpatterns = [
    path('projects/', views.ProjectsView.as_view(), name='porjects'),
    path('projects/<int:pk>/', views.ProjectDetailView.as_view(), name='porject'),
]
