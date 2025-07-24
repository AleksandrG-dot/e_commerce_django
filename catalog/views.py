from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
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
        """Если нет прав на изменение is_published, то не отображаем только разрешенные для публикации страницы"""
        if self.request.user.has_perm('catalog.can_unpublish_product'):
            return super().get_queryset()
        else:
            return Product.objects.filter(is_published=True)


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    context_object_name = "product"


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:home")


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        return reverse_lazy("catalog:product_detail", kwargs={"pk": self.object.pk})

    # По этому коду модератор сможет написать свою статью,
    # но не сможет её отредактировать, а только включить или отключить отображение
    def get_form_class(self):
        """ Если у пользователя есть право публиковать продукты, то выводится форма ProductModeratorForm"""
        user = self.request.user
        if user.has_perm("catalog.can_unpublish_product"):
            return ProductModeratorForm
        else:
            return super().get_form_class()


class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy("catalog:home")
    permission_required = 'catalog.delete_product'


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
