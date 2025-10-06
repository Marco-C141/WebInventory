from django.urls import path, include

from .views import products_list, products_add, categories_add, products_edit, categories_edit, products_delete, \
    categories_delete

urlpatterns = [
    path("products/", products_list, name="products_list"),
    path("products/add", products_add, name="product_add"),
    path("products/edit/<int:pk>/", products_edit, name="product_edit"),
    path("products/delete/<int:pk>/", products_delete, name="product_delete"),

    path("categories/add", categories_add, name="categories_add"),
    path("categories/edit/<int:pk>/", categories_edit, name="category_edit"),
    path("categories/delete/<int:pk>/", categories_delete, name="category_delete"),

    path("products/add", products_add, name="sell"),
    path("products/", products_list, name="dashboard")
]