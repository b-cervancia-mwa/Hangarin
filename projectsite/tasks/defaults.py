from datetime import timedelta

from django.utils import timezone

from tasks.models import Category, Note, Priority, SubTask, Task


DEFAULT_PRIORITY_NAMES = ["high", "medium", "low", "critical", "optional"]
DEFAULT_CATEGORY_NAMES = ["Work", "School", "Personal", "Finance", "Projects"]
STARTER_TASK_TITLE = "Review Hangarin starter data"
STARTER_SUBTASK_TITLE = "Check seeded starter records"
STARTER_NOTE_CONTENT = (
    "Starter note: verify the seeded categories, priorities, and task "
    "records before adding your own project data."
)


def ensure_default_workspace_data():
    priorities = {
        name: Priority.objects.get_or_create(name=name)[0]
        for name in DEFAULT_PRIORITY_NAMES
    }
    categories = {
        name: Category.objects.get_or_create(name=name)[0]
        for name in DEFAULT_CATEGORY_NAMES
    }

    starter_task = Task.objects.filter(title=STARTER_TASK_TITLE).first()

    if starter_task is None:
        starter_task = Task.objects.create(
            title=STARTER_TASK_TITLE,
            description=(
                "Confirm the required default priorities and categories exist "
                "before adding more task records."
            ),
            status="Pending",
            deadline=timezone.now() + timedelta(days=7),
            priority=priorities["high"],
            category=categories["Projects"],
        )

    if not SubTask.objects.exists():
        SubTask.objects.create(
            task=starter_task,
            title=STARTER_SUBTASK_TITLE,
            status="Pending",
        )

    if not Note.objects.exists():
        Note.objects.create(
            task=starter_task,
            content=STARTER_NOTE_CONTENT,
        )
