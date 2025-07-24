from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Create group product_moderator and users"

    def handle(self, *args, **kwargs):
        # Создание группы "Модератор продуктов"
        product_moderator_group, _ = Group.objects.get_or_create(
            name="product_moderator"
        )

        can_unpublish_product_perm = Permission.objects.get(
            codename="can_unpublish_product"
        )
        can_delete_product_perm = Permission.objects.get(codename="delete_product")

        product_moderator_group.permissions.add(
            can_unpublish_product_perm, can_delete_product_perm
        )

        # Создание пользователя mod@skystore.ru, принадлежащего группе "Модератор продуктов"
        User = get_user_model()
        user, _ = User.objects.get_or_create(email="mod@skystore.ru")
        user.set_password("123qwe")
        user.is_active = True
        user.is_staff = user.is_superuser = False
        user.groups.add(product_moderator_group)
        user.save()
        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created user with email {user.email} in product_moderator_group"
            )
        )

        # Создание обычного пользователя user@skystore.ru
        user2, _ = User.objects.get_or_create(email="user@skystore.ru")
        user2.set_password("123qwe")
        user2.is_active = True
        user2.is_staff = user.is_superuser = False
        user2.save()
        self.stdout.write(
            self.style.SUCCESS(f"Successfully created user with email {user.email}")
        )
