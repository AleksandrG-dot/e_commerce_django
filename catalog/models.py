from django.db import models

# В приложении каталога создайте модели Product и Category и опишите для них базовые настройки.
#
# Описание моделей:
# Product: наименование, описание, изображение, категория, цена за покупку,
# дата создания, дата последнего изменения.
#
# Category: наименование, описание.


class Category:
    name = models.CharField(
        max_length=150,
        verbose_name="Категория товара",
        help_text="Введите наименование категории товара",
        unique=True,
        null=False,
        blank=False
    )
    description = models.TextField(
        verbose_name="Описание категории",
        help_text="Введите описание категории",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]


class Product(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name="Наименование",
        help_text="Введите наименование продукта",
        null=False,
        blank=False
    )
    description = models.TextField(
        verbose_name="Описание товара",
        help_text="Введите описание товара",
        blank=True,
        null=True,
    )
    photo = models.ImageField(
        upload_to="Products/photos/",
        blank=True,
        null=True,
        verbose_name="Фотография продукта",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Категория",
        help_text="Введите категорию",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена за покупку",
        help_text="Введите цену",
    )
    created_at = models.DateField(
        verbose_name="Дата создания", auto_now_add=True, help_text="Дата создания"
    )
    updated_at = models.DateField(
        verbose_name="Дата последнего изменения",
        auto_now=True,
        help_text="Дата последнего изменения",
    )

    def __str__(self):
        return f"{self.name} {self.category} {self.price}"

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["name", "price"]
