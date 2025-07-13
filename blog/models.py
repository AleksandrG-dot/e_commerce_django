from django.db import models

# ДЗ №25 FBV и CBV
# Создайте новое приложение для блога и добавьте его в файл settings.py
# Создайте новую модель блоговой записи со следующими полями:
# - заголовок,
# - содержимое,
# - превью (изображение),
# - дата создания,
# - признак публикации (булевое поле),
# - количество просмотров.
# Для работы с блогом реализуйте полный CRUD для новой модели, используя CBV.


class BlogPost(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="Заголовок",
        help_text="Введите заголовок блога",
        null=False,
        blank=False,
    )
    content = models.TextField(
        verbose_name="Содержимое",
        help_text="Введите текст",
        blank=False,
        null=True,
    )
    preview = models.ImageField(
        upload_to="Blogs/preview/",
        blank=True,
        null=True,
        verbose_name="Превью блога",
    )
    created_at = models.DateField(
        verbose_name="Дата создания", auto_now_add=True, help_text="Дата создания"
    )
    is_published = models.BooleanField(
        default=False, verbose_name="Признак публикации", help_text="Опубликовано?"
    )

    views_counter = models.IntegerField(
        default=0, verbose_name="Просмотров", help_text="Количество просмотров блога"
    )

    def __str__(self):
        return f"{self.title}, {self.is_published}, {self.views_counter}"

    class Meta:
        verbose_name = "Блог"
        verbose_name_plural = "Блоги"
        ordering = ["created_at"]
