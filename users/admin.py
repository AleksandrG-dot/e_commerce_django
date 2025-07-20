from django.contrib import admin

from users.models import UserModel


@admin.register(UserModel)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "first_name", "last_name", "country", "phone", "avatar", "password", )
    search_fields = ("email",)
