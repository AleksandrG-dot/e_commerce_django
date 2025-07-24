from django import forms
from django.forms import ValidationError, BooleanField
from profanityfilter import ProfanityFilter

from catalog.models import Product
from config.settings import FORBIDDEN_WORDS


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class']="form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"
            # if field.help_text:
            #     field.widget.attrs["placeholder"] = field.help_text


class ProductModeratorForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = ("is_published", )


class ProductForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = ("category", "name", "price", "description", "photo")

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price <= 0:
            raise ValidationError("Цена не может быть отрицательной")
        return price

    def clean_photo(self):
        photo = self.cleaned_data.get("photo")
        if photo and not photo.closed:
            if photo.content_type not in ("image/jpeg", "image/png"):
                raise ValidationError("Формат файла должен быть JPEG или PNG")
            if photo.size > 5242880:
                raise ValidationError(
                    "Размер файла для загрузки не должен превышать 5 МБ"
                )
        return photo

    def clean_name(self):
        name = self.cleaned_data.get("name").lower()
        pf_custom = ProfanityFilter(custom_censor_list=FORBIDDEN_WORDS)
        if not pf_custom.is_clean(name):
            raise ValidationError(
                "В наименование товара присутствуют запрещенные слова"
            )
        return name

    def clean_description(self):
        description = self.cleaned_data.get("description")
        pf_custom = ProfanityFilter(custom_censor_list=FORBIDDEN_WORDS)
        if not pf_custom.is_clean(description):
            raise ValidationError("В описании товара присутствуют запрещенные слова")
        return description


class ContactForm(forms.Form):
    name = forms.CharField(max_length=150)
    phone_number = forms.CharField(max_length=15)
    message = forms.CharField(widget=forms.Textarea)
