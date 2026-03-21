from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
import random

from tasks.models import Task, SubTask, Note, Priority, Category


class Command(BaseCommand):
    help = "Seed fake data for Task, SubTask, and Note"

    def handle(self, *args, **kwargs):
        fake = Faker()

        priorities = list(Priority.objects.all())
        categories = list(Category.objects.all())

        if not priorities or not categories:
            self.stdout.write(self.style.ERROR(
                "Please add Priority and Category records first in admin."
            ))
            return

        for _ in range(20):
            task = Task.objects.create(
                title=fake.sentence(nb_words=5),
                description=fake.paragraph(nb_sentences=3),
                status=fake.random_element(elements=["Pending", "In Progress", "Completed"]),
                deadline=timezone.make_aware(fake.date_time_this_month()),
                priority=random.choice(priorities),
                category=random.choice(categories),
            )

            for _ in range(random.randint(1, 3)):
                SubTask.objects.create(
                    task=task,
                    title=fake.sentence(nb_words=4),
                    status=fake.random_element(elements=["Pending", "In Progress", "Completed"]),
                )

            for _ in range(random.randint(1, 2)):
                Note.objects.create(
                    task=task,
                    content=fake.paragraph(nb_sentences=2),
                )

        self.stdout.write(self.style.SUCCESS("Fake data generated successfully."))