from rest_framework import serializers

from tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "title", "description", "is_done", "created_at"]
        read_only_fields = ["id", "is_done", "created_at"]


class TaskCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100, allow_blank=False, trim_whitespace=True)
    description = serializers.CharField(required=False, allow_blank=True, default="")
