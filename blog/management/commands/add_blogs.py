from django.core.management import call_command
from django.core.management.base import BaseCommand

from blog.models import BlogPost


class Command(BaseCommand):
    help = "Load blog data from fixture"

    def handle(self, *args, **kwargs):
        # Удаляем существующие записи
        BlogPost.objects.all().delete()

        # Загружаем данные из фикстуры blog.json c BlogPost
        call_command("loaddata", "blog.json")
        self.stdout.write(self.style.SUCCESS("Successfully loaded data from fixture"))
