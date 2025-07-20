from django.contrib import admin

from users.models import UserModel


@admin.register(UserModel)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "password", "country", "phone", "avatar")
    search_fields = ("email",)
