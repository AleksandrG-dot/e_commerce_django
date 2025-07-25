from django.contrib.auth.forms import UserCreationForm
from django import forms

from catalog.forms import StyleFormMixin
from users.models import UserModel


class UserCreateForm(StyleFormMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = (
            "email",
            "password1",
            "password2",
        )


class UserUpdateForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = UserModel
        fields = (
            "first_name",
            "last_name",
            "phone",
            "country",
            "avatar",
        )
