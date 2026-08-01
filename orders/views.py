from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from cart.models import Cart
from .models import Order, OrderItem
from .forms import CheckoutForm


@login_required
def checkout(request):

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    if not cart.items.exists():
        return redirect("cart")

    if request.method == "POST":

        form = CheckoutForm(request.POST)

        if form.is_valid():

            order = form.save(commit=False)

            order.user = request.user
            order.total_price = 0
            order.save()

            total = 0

            for item in cart.items.all():

                # Kiểm tra tồn kho
                if item.product.stock < item.quantity:
                    return redirect("cart")

                # Lưu sản phẩm vào đơn hàng
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )

                # Trừ tồn kho
                product = item.product
                product.stock -= item.quantity
                product.save()

                # Tính tổng tiền
                total += item.product.price * item.quantity

            order.total_price = total
            order.save()

            # Xóa giỏ hàng
            cart.items.all().delete()

            return redirect("my_orders")

    else:

        form = CheckoutForm()

    return render(
        request,
        "orders/checkout.html",
        {
            "form": form,
            "cart": cart,
        }
    )


@login_required
def my_orders(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by(
        "-created_at"
    )

    return render(
        request,
        "orders/my_orders.html",
        {
            "orders": orders,
        }
    )