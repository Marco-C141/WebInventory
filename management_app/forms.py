import os

from django import forms
from django.core.files import File

from project import settings
from .models import Product, Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "category", "price", "stock", "img"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].label = "Nombre del producto"
        self.fields['category'].label = "Categoría"
        self.fields['category'].empty_label = "Selecciona una categoría"
        self.fields['price'].label = "Precio"
        self.fields['stock'].label = "Unidades disponibles"
        self.fields['img'].label = "Imagen del producto"

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].label = "Nombre de la categoría"