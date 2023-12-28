from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from django.http import HttpResponse
from .models import Product, Customer, Cart, CartItem, Category, Order, OrderItem
from .forms import CheckoutForm


# Create your views here.
class ProductListView(View):
    template_name = "product_list.html"

    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        return render(request, self.template_name, {"products": products})


class ProductDetailView(View):
    template_name = "product_detail.html"

    def get(self, request, pk, *args, **kwargs):
        product = get_object_or_404(Product, pk=pk)
        return render(request, self.template_name, {"product": product})


# function based views


def category_page(request, category_id):
    category = Category.objects.get(pk=category_id)
    products = Product.objects.filter(category=category)

    context = {
        "category": category,
        "products": products,
    }

    return render(request, "category_page.html", context)


def product_list(request):
    products = Product.objects.all()
    return render(request, "product_list.html", {"products": products})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    customer = Customer.objects.get(user=request.user)
    return render(request, "product_detail.html", {"product": product})


@login_required
def add_to_cart(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        quantity = int(request.POST.get("quantity", 1))

        product = Product.objects.get(pk=product_id)
        customer = Customer.objects.get(user=request.user)

        customer.cart.add_to_cart(product, quantity)

    return redirect("product_detail", pk=product_id)


@login_required
def remove_from_cart(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")

        product = Product.objects.get(pk=product_id)
        customer = Customer.objects.get(user=request.user)

        customer.cart.remove_from_cart(product)

    return redirect("product_detail", pk=product_id)


@login_required
def remove_single_item_from_cart(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")

        product = Product.objects.get(pk=product_id)
        customer = Customer.objects.get(user=request.user)

        customer.cart.remove_single_item_from_cart(product)

    return redirect("product_detail", pk=product_id)


@login_required
def view_cart(request):
    customer = Customer.objects.get(user=request.user)
    return render(request, "cart/view_cart.html", {"cart": customer.cart})


@login_required
def clear_cart(request):
    customer = Customer.objects.get(user=request.user)
    customer.cart.clear_cart()
    return redirect("view_cart")


@login_required
def checkout(request):
    customer = Customer.objects.get(user=request.user)
    cart = customer.cart

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Assuming your form includes fields like 'address', 'phone_number', etc.
            order = Order.objects.create(customer=customer, **form.cleaned_data)
            order.create_order(cart)
            return redirect("order_confirmation", pk=order.pk)
    else:
        form = CheckoutForm()

    return render(request, "checkout.html", {"form": form, "cart": cart})


@login_required
def order_confirmation(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, "order_confirmation.html", {"order": order})
