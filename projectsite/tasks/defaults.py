from datetime import timedelta

from django.utils import timezone

from tasks.models import Category, Note, Priority, SubTask, Task


DEFAULT_PRIORITY_NAMES = ["high", "medium", "low", "critical", "optional"]
DEFAULT_CATEGORY_NAMES = ["Work", "School", "Personal", "Finance", "Projects"]

DEFAULT_WORKSPACE_TASKS = [
    {
        "title": "Review Hangarin starter data",
        "description": (
            "Confirm the required default priorities and categories exist "
            "before adding more task records."
        ),
        "status": "Pending",
        "days_from_now": 7,
        "priority": "high",
        "category": "Projects",
        "subtasks": [
            {"title": "Check seeded starter records", "status": "Pending"},
            {"title": "Verify dashboard starter widgets", "status": "Pending"},
        ],
        "note": (
            "Starter note: verify the seeded categories, priorities, and task "
            "records before adding your own project data."
        ),
    },
    {
        "title": "Prepare team meeting agenda",
        "description": (
            "Outline the status updates, open blockers, and owner assignments "
            "for the next work sync."
        ),
        "status": "Pending",
        "days_from_now": 2,
        "priority": "critical",
        "category": "Work",
        "subtasks": [
            {"title": "Draft the key agenda topics", "status": "Completed"},
            {"title": "Attach the deployment notes", "status": "Pending"},
        ],
        "note": "Add deployment blockers and budget review items before the meeting starts.",
    },
    {
        "title": "Plan weekly academic deadlines",
        "description": (
            "Review the current school deliverables and block focused study "
            "time for the nearest due dates."
        ),
        "status": "In Progress",
        "days_from_now": 1,
        "priority": "medium",
        "category": "School",
        "subtasks": [
            {"title": "List remaining coursework", "status": "Completed"},
            {"title": "Reserve evening study hours", "status": "In Progress"},
        ],
        "note": "Double-check the research outline deadline and submit the draft before Wednesday.",
    },
    {
        "title": "Organize personal errands",
        "description": (
            "Group the personal errands that can be finished in one trip and "
            "set realistic time blocks for them."
        ),
        "status": "In Progress",
        "days_from_now": 3,
        "priority": "optional",
        "category": "Personal",
        "subtasks": [
            {"title": "Finalize the errands checklist", "status": "Pending"},
        ],
        "note": "Buy household supplies and schedule the weekend pickup while you are already outside.",
    },
    {
        "title": "Submit allowance tracker update",
        "description": (
            "Record the latest expenses and publish the refreshed finance "
            "tracker summary for the week."
        ),
        "status": "Completed",
        "days_from_now": 4,
        "priority": "low",
        "category": "Finance",
        "subtasks": [
            {"title": "Categorize the latest receipts", "status": "Completed"},
        ],
        "note": "Archive the finalized tracker sheet after sending the updated summary.",
    },
    {
        "title": "Finalize project milestone board",
        "description": (
            "Refresh the milestone board so the project timeline, owners, and "
            "next deliverables are visible to the whole team."
        ),
        "status": "Pending",
        "days_from_now": 5,
        "priority": "critical",
        "category": "Projects",
        "subtasks": [
            {"title": "Review open milestone cards", "status": "In Progress"},
            {"title": "Mark completed deliverables", "status": "Pending"},
        ],
        "note": "Highlight the next release checkpoint and clean up stale project cards.",
    },
]

DEFAULT_WORKSPACE_TITLES = [item["title"] for item in DEFAULT_WORKSPACE_TASKS]


def _ensure_default_lookups():
    priorities = {
        name: Priority.objects.get_or_create(name=name)[0]
        for name in DEFAULT_PRIORITY_NAMES
    }
    categories = {
        name: Category.objects.get_or_create(name=name)[0]
        for name in DEFAULT_CATEGORY_NAMES
    }
    return priorities, categories


def _create_seeded_workspace(priorities, categories):
    for blueprint in DEFAULT_WORKSPACE_TASKS:
        task, _ = Task.objects.get_or_create(
            title=blueprint["title"],
            defaults={
                "description": blueprint["description"],
                "status": blueprint["status"],
                "deadline": timezone.now() + timedelta(days=blueprint["days_from_now"]),
                "priority": priorities[blueprint["priority"]],
                "category": categories[blueprint["category"]],
            },
        )

        for subtask_data in blueprint["subtasks"]:
            SubTask.objects.get_or_create(
                task=task,
                title=subtask_data["title"],
                defaults={"status": subtask_data["status"]},
            )

        Note.objects.get_or_create(
            task=task,
            content=blueprint["note"],
        )


def ensure_default_workspace_data():
    priorities, categories = _ensure_default_lookups()

    has_user_tasks = Task.objects.exclude(title__in=DEFAULT_WORKSPACE_TITLES).exists()

    if not has_user_tasks:
        _create_seeded_workspace(priorities, categories)
        return

    if not Task.objects.exists():
        _create_seeded_workspace(priorities, categories)
