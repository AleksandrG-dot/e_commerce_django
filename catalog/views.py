from django import forms
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView
from catalog.models import Product


class ProductListView(ListView):
    model = Product


class ProductDetailView(DetailView):
    model = Product
    context_object_name = "product"


class ContactForm(forms.Form):
    pass
    # name = forms.CharField(max_length=150)
    # phone_number = forms.CharField(max_length=15)
    # message = forms.CharField(widget=forms.Textarea)


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
