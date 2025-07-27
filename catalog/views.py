from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import (
    ListView,
    DetailView,
    FormView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
)

from .services import ProductService

from catalog.forms import ContactForm, ProductForm, ProductModeratorForm
from catalog.models import Product, Category


class ProductByCategoryList(TemplateView):
    model = Category
    template_name = r"catalog\prod_by_category_list.html"
    context_object_name = "categories"

    def get_context_data(self, **kwargs):
        """Передает данные для формы"""
        context = super().get_context_data(**kwargs)

        # Заносим в контекст набор существующих категорий т.к. TeplateView этого не делает
        context[self.context_object_name] = Category.objects.all()

        # Заносим в контекст id выбранной категории (для его выбора в выпадающем меню)
        context["selected_category"] = self.kwargs.get("pk", None)

        # Забираем продукты из требуемой категории с использованием сервисной функции,
        # которая на вход принимает требуемую категорию. ID категории забираем из pk от URl-запроса
        products = ProductService.get_products_by_category(
            Category(id=self.kwargs["pk"])
        )

        # Если у пользователя нет права изменять публикацию продукта (can_unpublish_product),
        # то фильтруем результат на отсутствие не публикуемых товаров
        if not self.request.user.has_perm("catalog.can_unpublish_product"):
            products = [prod for prod in products if prod.is_published]

        # Заносим в контекст список продуктов
        context["products"] = products
        return context

    def post(self, request, *args, **kwargs):
        """Метод post теперь перенаправляет на страницу продуктов по категории с выбранной пользователем категорией"""
        pk = request.POST.get("cetegory_select")
        if not pk.isdigit():
            pk = "0"
        return redirect(
            reverse_lazy("catalog:product_by_category", kwargs={"pk": int(pk)})
        )


class ProductListView(ListView):
    model = Product

    def get_queryset(self):
        """Если нет прав на изменение is_published, то отображаем только разрешенные для публикации страницы.
        Есть кеширование"""
        key_pub = 'product_is_published' # ключ кеширования для опубликованных продуктов
        if self.request.user.has_perm("catalog.can_unpublish_product"):
            return super().get_queryset().order_by("is_published")
        else:
            # Кеширую только запросы для пользователей без прав публикации.
            # Если кешировать для тех у кого есть права, они могут видеть не верную инфу и это критично
            queryset = cache.get(key_pub)
            if not queryset:
                queryset = Product.objects.filter(is_published=True)
                cache.set(key_pub, queryset, 900)
            return queryset


@method_decorator(cache_page(900), name="dispatch")
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
    template_name = r"catalog\contacts.html"
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
