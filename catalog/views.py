from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    FormView,
    CreateView,
    UpdateView,
    DeleteView,
)

from catalog.forms import ContactForm, ProductForm, ProductModeratorForm
from catalog.models import Product


class ProductListView(ListView):
    model = Product

    def get_queryset(self):
        """Если нет прав на изменение is_published, то отображаем только разрешенные для публикации страницы"""
        if self.request.user.has_perm("catalog.can_unpublish_product"):
            return super().get_queryset().order_by("is_published")
        else:
            return Product.objects.filter(is_published=True)


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    context_object_name = "product"


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:home")

    def form_valid(self, form):
        """Присваивает полю владельца продукта текущего авторизованного пользователя"""
        product = form.save()
        user = self.request.user
        product.owner = user
        product.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        return reverse_lazy("catalog:product_detail", kwargs={"pk": self.object.pk})

    def get_form_class(self):
        """
        Если у пользователя есть право публиковать продукты, то выводится форма ProductModeratorForm,
        дающая только права на публикацию (без возможности редактирования самого продукта)
        """
        user = self.request.user
        # Если этот продукт пользователя с правом публиковать продукты,
        # то он не может сам его опубликовать, а только отредактировать.
        if (
            user.has_perm("catalog.can_unpublish_product")
            and not user == self.object.owner
        ):
            return ProductModeratorForm
        else:
            return super().get_form_class()

    def test_func(self):
        """
        UserPassesTestMixin даёт возможность редактировать продукт только его владельцу и пользователю
        с правами на публикацию
        """
        return (
            self.request.user == self.get_object().owner
            or self.request.user.has_perm("catalog.can_unpublish_product")
        )


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    success_url = reverse_lazy("catalog:home")

    def test_func(self):
        """
        UserPassesTestMixin даёт возможность удалять продукт только его владельцу и пользователю
        с правами на удаление
        """
        return (
            self.request.user == self.get_object().owner
            or self.request.user.has_perm("catalog.delete_product")
        )


class ContactsView(FormView):
    template_name = "catalog/contacts.html"
    form_class = ContactForm
    success_url = reverse_lazy("catalog:contacts")

    def post(self, request, *args, **kwargs):
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено.")

    # def form_valid(self, form):
    #     name = form.cleaned_data['name']
    #     return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено.") #super().form_valid(form)
