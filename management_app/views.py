from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from .models import Category, Product
from .forms import CategoryForm, ProductForm


class CustomLoginView(LoginView):
    """ Allows redirection based on the users' role"""
    template_name = "registration/login.html"

    def get_success_url(self):
        user = self.request.user

        if user.is_superuser:
            return reverse_lazy("admin:index")

        if user.is_staff:
            return reverse_lazy("products_list")

        return reverse_lazy("home")


@login_required
def products_list(request):
    """ This method returns all products grouped by category in a map

    :param request:
    :return:
    """
    categories = Category.objects.all()
    products = {}

    for category in categories:
        products_in_category = Product.objects.filter(category=category)
        products[category] = products_in_category

    context = {
        "products": products
    }

    return render(request, "management_app/products.html", context)


@login_required()
def products_add(request):
    """ This method redirects the user to the create product form template, or process the submitted form """
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("products_list")

    form = ProductForm()

    return render(request, "management_app/products-form.html", {"form": form})

@login_required()
def products_edit(request, pk):
    """ This method prepopulates the form with the product's data and returns the create template """
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products_list')
    else:
        form = ProductForm(instance=product)

    context = {
        "form": form,
    }

    return render(request, "management_app/products-form.html", context)

@login_required()
def products_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.delete()
        return redirect('products_list')

    return render(request, 'management_app/object-delete.html', {'object': product})


@login_required()
def categories_add(request):
    """ This method redirects the user to the create category form template, or process the submitted form """
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("products_list")

    form = CategoryForm()

    return render(request, "management_app/categories-form.html", {"form": form})


@login_required()
def categories_edit(request, pk):
    """ This method prepopulates the form with the category's data and returns the "create" template """
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('products_list')

    form = CategoryForm(instance=category)

    return render(request, "management_app/categories-form.html", {"form": form})

@login_required()
def categories_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        category.delete()
        return redirect('products_list')

    return render(request, 'management_app/object-delete.html', {'object': category})
