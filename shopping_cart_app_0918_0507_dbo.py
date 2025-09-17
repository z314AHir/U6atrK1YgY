# 代码生成时间: 2025-09-18 05:07:23
# shopping_cart_app/models.py
"""
Define the models for the shopping cart application.
"""
from django.db import models
def get_default_user():
    # Implement logic to get the default user
    pass

class Product(models.Model):
    """
    Represents a product that can be added to the shopping cart.
    """
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()

    def __str__(self):
        return self.name

class Cart(models.Model):
    """
    Represents a shopping cart.
    """
    user = models.OneToOneField(get_default_user(), on_delete=models.CASCADE)
    items = models.ManyToManyField(Product, through='CartItem', blank=True)

    def __str__(self):
        return f"{self.user.username}'s cart"

class CartItem(models.Model):
    """
    Represents an item in the shopping cart.
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    class Meta:
        unique_together = ('cart', 'product')

# shopping_cart_app/views.py
"""
Define the views for the shopping cart application.
"""
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Cart, CartItem, Product

def cart_detail(request, cart_id):
    """
    Return the details of a specific cart.
    """
    try:
        cart = Cart.objects.get(pk=cart_id)
    except Cart.DoesNotExist:
        raise Http404("Cart does not exist")
    return render(request, 'shopping_cart/cart_detail.html', {'cart': cart})

def add_to_cart(request, product_id):
    "