from django.urls import path
from .views import (
    product_detail,
    view_cart,
    product_list,
    add_to_cart,
    remove_from_cart,
    remove_single_item_from_cart,
    clear_cart,
    order_confirmation,
    checkout,
)


urlpatterns = [
    # Function-Based Views
    path("products/", product_list, name="product_list"),
    path("products/<int:pk>/", product_detail, name="product_detail"),
    path("add_to_cart/", add_to_cart, name="add_to_cart"),
    path("remove_from_cart/", remove_from_cart, name="remove_from_cart"),
    path(
        "remove_single_item_from_cart/",
        remove_single_item_from_cart,
        name="remove_single_item_from_cart",
    ),
    path("view_cart/", view_cart, name="view_cart"),
    path("clear_cart/", clear_cart, name="clear_cart"),
    path("checkout/", checkout, name="checkout"),
    path("order_confirmation/<int:pk>/", order_confirmation, name="order_confirmation"),
    # other URLs...
    # other URLs...
]
