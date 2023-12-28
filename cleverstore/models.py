from django.db import models
from django.urls import reverse
from authentication.models import CustomUser


class Customer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.TextField()
    phone_number = models.CharField(max_length=20)
    wishlist = models.ManyToManyField(
        "Product", related_name="wishlisted_by", blank=True
    )


class Category(models.Model):
    name = models.CharField(max_length=255)
    parent_category = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE
    )

    def get_absolute_url(self):
        return reverse("category_page", args=[str(self.id)])


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="product_images/", null=True, blank=True)
    rating = models.FloatField(default=0)

    def get_absolute_url(self):
        return reverse("product_detail", args=[str(self.id)])


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    is_shipped = models.BooleanField(default=False)

    def create_order(self, cart):
        order = Order.objects.create(customer=self.customer)
        for cart_item in cart.cartitem_set.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                item_price=cart_item.product.price,
            )
            order.total_amount += cart_item.product.price * cart_item.quantity
        order.save()
        cart.clear_cart()
        return order


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    item_price = models.DecimalField(max_digits=10, decimal_places=2)


class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=255)


class Shipment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    tracking_number = models.CharField(max_length=255)
    shipment_date = models.DateTimeField(auto_now_add=True)
    address = models.TextField()


class Cart(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through="CartItem")

    def add_to_cart(self, product, quantity=1):
        cart_item, created = CartItem.objects.get_or_create(cart=self, product=product)
        if not created:
            cart_item.quantity += quantity
            cart_item.save()

    def remove_from_cart(self, product):
        cart_item = CartItem.objects.get(cart=self, product=product)
        cart_item.delete()

    def remove_single_item_from_cart(self, product):
        cart_item = CartItem.objects.get(cart=self, product=product)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

    def clear_cart(self):
        self.products.clear()


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()


class Wishlist(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
