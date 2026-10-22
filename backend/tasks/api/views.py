from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from tasks.application.commands import create_task, delete_task, toggle_task
from tasks.application.exceptions import InvalidTaskStatusFilterError
from tasks.application.queries import list_tasks
from tasks.models import Task

from .serializers import TaskCreateSerializer, TaskSerializer


class TaskListCreateView(APIView):
    """GET: 一覧 / POST: 作成"""

    def get(self, request: Request) -> Response:
        status_filter = request.query_params.get("status", "open")
        try:
            tasks = list_tasks(status_filter)
        except InvalidTaskStatusFilterError:
            return Response(
                {"detail": "status は all, open, done のいずれかです。"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        serializer = TaskCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = create_task(
            title=serializer.validated_data["title"],
            description=serializer.validated_data.get("description", ""),
        )
        return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)


class TaskToggleView(APIView):
    def post(self, request: Request, pk: int) -> Response:
        task = get_object_or_404(Task, pk=pk)
        task = toggle_task(task)
        return Response(TaskSerializer(task).data)


class TaskDetailView(APIView):
    def delete(self, request: Request, pk: int) -> Response:
        task = get_object_or_404(Task, pk=pk)
        delete_task(task)
        return Response(status=status.HTTP_204_NO_CONTENT)
