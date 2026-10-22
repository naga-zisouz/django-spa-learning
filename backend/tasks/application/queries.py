from django.db.models import QuerySet

from tasks.application.exceptions import InvalidTaskStatusFilterError
from tasks.models import Task

VALID_STATUS_FILTERS = frozenset({"all", "open", "done"})


def list_tasks(status: str = "open") -> QuerySet[Task]:
    """status に応じてタスク一覧を返す。"""
    if status not in VALID_STATUS_FILTERS:
        raise InvalidTaskStatusFilterError(f"Unknown status filter: {status}")

    queryset = Task.objects.all()
    if status == "open":
        queryset = queryset.filter(is_done=False)
    elif status == "done":
        queryset = queryset.filter(is_done=True)
    return queryset
