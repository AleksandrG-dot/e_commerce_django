from django.core.management import call_command
from django.core.management.base import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    help = "Load test data from fixture"

    def handle(self, *args, **kwargs):
        # Удаляем существующие записи
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Загружаем данные из фикстуры catalog.json c Category и Product
        call_command("loaddata", "catalog.json")
        self.stdout.write(self.style.SUCCESS("Successfully loaded data from fixture"))
