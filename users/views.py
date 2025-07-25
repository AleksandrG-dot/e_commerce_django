from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from config.settings import EMAIL_HOST_USER
from users.forms import UserCreateForm, UserUpdateForm
from users.models import UserModel


class UserCreateView(CreateView):
    model = UserModel
    template_name = "register.html"
    form_class = UserCreateForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        password = form.cleaned_data.get("password1")
        user = form.save()
        self.send_welcome_email(user.email, password)
        return super().form_valid(form)

    def send_welcome_email(self, user_email, password):
        subject = "Спасибо за регистрацию в SkyStore"
        message = f"""Добро пожаловать на торговую площадку SkyStore.
Здесь вы можете найти товары на любой вкус.
Ваш пароль: {password}"""
        from_email = EMAIL_HOST_USER
        recipient_list = [user_email]
        send_mail(subject, message, from_email, recipient_list)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = UserModel
    template_name = "update.html"
    form_class = UserUpdateForm

    def get_success_url(self):
        return reverse_lazy("users:update", kwargs={"pk": self.object.pk})
