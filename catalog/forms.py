from django import forms
from django.forms import ValidationError
from profanityfilter import ProfanityFilter

from catalog.models import Product

FORBIDDEN_WORDS = [
    "казино",
    "криптовалюта",
    "крипта",
    "биржа",
    "дешево",
    "бесплатно",
    "обман",
    "полиция",
    "радар",
]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ("category", "name", "price", "description", "photo")

    def clean(self):
        cleaned_data = super().clean()
        content = (
            cleaned_data.get("name").lower()
            + " "
            + cleaned_data.get("description").lower()
        )
        pf_custom = ProfanityFilter(custom_censor_list=FORBIDDEN_WORDS)
        if not pf_custom.is_clean(content):
            raise ValidationError("В описании присутствуют запрещенные слова")


class ContactForm(forms.Form):
    name = forms.CharField(max_length=150)
    phone_number = forms.CharField(max_length=15)
    message = forms.CharField(widget=forms.Textarea)
