from django.urls import path

from . import views

app_name = "tasks_api"

urlpatterns = [
    path("tasks/", views.TaskListCreateView.as_view(), name="task-list"),
    path("tasks/<int:pk>/toggle/", views.TaskToggleView.as_view(), name="task-toggle"),
    path("tasks/<int:pk>/", views.TaskDetailView.as_view(), name="task-detail"),
]
