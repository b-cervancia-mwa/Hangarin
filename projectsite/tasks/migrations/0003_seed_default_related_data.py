from django.db import migrations


STARTER_SUBTASK_TITLE = "Check seeded starter records"
STARTER_NOTE_CONTENT = (
    "Starter note: verify the seeded categories, priorities, and task "
    "records before adding your own project data."
)


def seed_default_related_data(apps, schema_editor):
    Task = apps.get_model("tasks", "Task")
    SubTask = apps.get_model("tasks", "SubTask")
    Note = apps.get_model("tasks", "Note")

    starter_task = Task.objects.filter(title="Review Hangarin starter data").first()
    if starter_task is None:
        return

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


class Migration(migrations.Migration):

    dependencies = [
        ("tasks", "0002_seed_default_data"),
    ]

    operations = [
        migrations.RunPython(seed_default_related_data, migrations.RunPython.noop),
    ]
