from datetime import timedelta

from django.db import migrations
from django.utils import timezone


def seed_default_data(apps, schema_editor):
    Category = apps.get_model("tasks", "Category")
    Priority = apps.get_model("tasks", "Priority")
    Task = apps.get_model("tasks", "Task")

    priority_names = ["high", "medium", "low", "critical", "optional"]
    category_names = ["Work", "School", "Personal", "Finance", "Projects"]

    priorities = {
        name: Priority.objects.get_or_create(name=name)[0]
        for name in priority_names
    }
    categories = {
        name: Category.objects.get_or_create(name=name)[0]
        for name in category_names
    }

    Task.objects.get_or_create(
        title="Review Hangarin starter data",
        defaults={
            "description": (
                "Confirm the required default priorities and categories exist "
                "before adding more task records."
            ),
            "status": "Pending",
            "deadline": timezone.now() + timedelta(days=7),
            "priority": priorities["high"],
            "category": categories["Projects"],
        },
    )


class Migration(migrations.Migration):

    dependencies = [
        ("tasks", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_default_data, migrations.RunPython.noop),
    ]
