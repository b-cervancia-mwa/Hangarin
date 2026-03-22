from datetime import timedelta

from django.utils import timezone

from tasks.models import Category, Priority, Task


DEFAULT_PRIORITY_NAMES = ["high", "medium", "low", "critical", "optional"]
DEFAULT_CATEGORY_NAMES = ["Work", "School", "Personal", "Finance", "Projects"]
STARTER_TASK_TITLE = "Review Hangarin starter data"


def ensure_default_workspace_data():
    priorities = {
        name: Priority.objects.get_or_create(name=name)[0]
        for name in DEFAULT_PRIORITY_NAMES
    }
    categories = {
        name: Category.objects.get_or_create(name=name)[0]
        for name in DEFAULT_CATEGORY_NAMES
    }

    if not Task.objects.exists():
        Task.objects.create(
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
