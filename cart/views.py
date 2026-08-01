from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Cart, CartItem
from products.models import Product


@login_required
def add_to_cart(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    # Hết hàng
    if product.stock <= 0:

        messages.error(
            request,
            "Sản phẩm đã hết hàng."
        )

        return redirect(
            "product_detail",
            slug=product.slug
        )

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if created:

        item.quantity = 1

    else:

        if item.quantity >= product.stock:

            messages.warning(
                request,
                "Đã đạt số lượng tồn kho."
            )

            return redirect("cart")

        item.quantity += 1

    item.save()

    messages.success(
        request,
        "Đã thêm vào giỏ hàng."
    )

    return redirect("cart")

@login_required
def buy_now(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    if product.stock <= 0:
        messages.error(request, "Sản phẩm đã hết hàng.")
        return redirect("product_detail", slug=product.slug)

    cart, created = Cart.objects.get_or_create(user=request.user)

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if created:
        item.quantity = 1
    else:
        if item.quantity < product.stock:
            item.quantity += 1

    item.save()

    return redirect("checkout")
@login_required
def cart_detail(request):

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    total = 0

    for item in cart.items.all():

        total += item.subtotal

    return render(
        request,
        "cart/cart.html",
        {
            "cart": cart,
            "total": total,
        }
    )


@login_required
def increase_quantity(request, item_id):

    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    if item.quantity < item.product.stock:

        item.quantity += 1
        item.save()

    else:

        messages.warning(
            request,
            "Không thể tăng thêm vì vượt tồn kho."
        )

    return redirect("cart")


@login_required
def decrease_quantity(request, item_id):

    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    if item.quantity > 1:

        item.quantity -= 1
        item.save()

    else:

        item.delete()

    return redirect("cart")


@login_required
def remove_item(request, item_id):

    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    item.delete()

    return redirect("cart")