from django.contrib.auth.forms import UserCreationForm

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
