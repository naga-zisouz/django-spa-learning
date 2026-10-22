from tasks.models import Task


def create_task(title: str, description: str = "") -> Task:
    return Task.objects.create(title=title.strip(), description=description.strip())


def toggle_task(task: Task) -> Task:
    task.is_done = not task.is_done
    task.save(update_fields=["is_done"])
    return task


def delete_task(task: Task) -> None:
    task.delete()
