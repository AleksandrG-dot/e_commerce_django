from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import (
    ProductListView,
    ProductDetailView,
    ContactsView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    ProductByCategoryList,
)

app_name = CatalogConfig.name

urlpatterns = [
    path("", ProductListView.as_view(), name="home"),
    path("contacts/", ContactsView.as_view(), name="contacts"),
    path("product/<int:pk>/detail/", ProductDetailView.as_view(), name="product_detail"),
    path("product/create/", ProductCreateView.as_view(), name="product_create"),
    path("product/<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"),
    path("product/<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"),
    path("category/<int:pk>/detail/", ProductByCategoryList.as_view(), name="product_by_category"),
]
