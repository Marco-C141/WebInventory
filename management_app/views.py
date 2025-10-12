import json

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
            return reverse_lazy("dashboard")

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
    next_url = request.GET.get('next')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            if next_url:
                return redirect(next_url)
            return redirect('products_list')
    else:
        form = ProductForm(instance=product)

    context = {
        "form": form,
        "next_url": next_url,
    }

    return render(request, "management_app/products-form.html", context)

@login_required()
def products_delete(request, pk):
    """ Redirects the user to a confirmation to delete the product or does the deletion """
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
    """ Asks the user for deletion confirmation then proceeds """
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        category.delete()
        return redirect('products_list')

    return render(request, 'management_app/object-delete.html', {'object': category})


@login_required()
def dashboard(request):
    """ This view should contain useful information for the owner, for now, it'll only contain products with
        stock less than 5
    """
    low_stock_products = Product.objects.filter(stock__lte=5)
    context = {
        "low_stock_products": low_stock_products,
    }
    return render(request, "management_app/dashboard.html", context)


@login_required()
def pos_view(request):
    """ Returns all products in a JSON list of dictionaries so JS can handle all display logic client side """
    products = Product.objects.filter(stock__gt=0)

    products_list = []
    for product in products:
        products_list.append({
            "id": product.id,
            "name": product.name,
            "stock": product.stock,
            "price": str(product.price),
            "img": product.img.url
        })

    products_json = json.dumps(products_list)
    context = {
        "products": products_json,
    }

    return render(request, "management_app/pos.html", context)


# management_app/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
import json


@csrf_exempt
@transaction.atomic
def process_sale(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

    try:
        data = json.loads(request.body)
        cart_items = data.get('cart', [])

        updated_products = []  # List to hold the updated data

        for item in cart_items:
            product = Product.objects.get(id=item['id'])
            if product.stock >= item['quantity']:
                product.stock -= item['quantity']
                product.save()
                # Add the product's new state to our list
                updated_products.append({
                    'id': product.id,
                    'new_stock': product.stock
                })
            else:
                return JsonResponse({'status': 'error', 'message': f'Not enough stock for {product.name}'},
                                    status=400)
        return JsonResponse({
            'status': 'success',
            'message': 'Sale completed successfully!',
            'updated_products': updated_products
        })

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

