from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.core.paginator import Paginator

from accounts.decorators import staff_required
from products.models import Product
from orders.models import Order
from categories.models import Category

from .forms import StaffProductForm


# ==========================
# Dashboard
# ==========================
@staff_required
def dashboard(request):

    latest_products = Product.objects.order_by(
        "-id"
    )[:5]

    latest_orders = Order.objects.select_related(
        "user"
    ).order_by(
        "-created_at"
    )[:5]

    low_stock_products = Product.objects.filter(
        stock__lt=10
    ).order_by(
        "stock"
    )[:5]

    pending = Order.objects.filter(
        status="pending"
    ).count()

    shipping = Order.objects.filter(
        status="shipping"
    ).count()

    completed = Order.objects.filter(
        status="completed"
    ).count()

    cancelled = Order.objects.filter(
        status="cancelled"
    ).count()
    confirmed = Order.objects.filter(
    status="confirmed"
    ).count()
    context = {

    "product_count": Product.objects.count(),

    "order_count": Order.objects.count(),

    "pending_count": pending,

    "shipping_count": shipping,

    "latest_products": latest_products,

    "latest_orders": latest_orders,

    "low_stock_products": low_stock_products,

    "pending": pending,

    "confirmed": confirmed,

    "shipping": shipping,

    "completed": completed,

    "cancelled": cancelled,

}
    return render(
        request,
        "staff/index.html",
        context
    )

# ==========================
# Product
# ==========================

@staff_required
def product_list(request):

    products = Product.objects.select_related(
        "category"
    ).order_by("-id")

    keyword = request.GET.get("keyword")

    if keyword:

        products = products.filter(
            name__icontains=keyword
        )

    category_id = request.GET.get("category")

    if category_id:

        products = products.filter(
            category_id=category_id
        )

    paginator = Paginator(
        products,
        10
    )

    page = request.GET.get("page")

    products = paginator.get_page(page)

    return render(
        request,
        "staff/product_list.html",
        {
            "products": products,
            "categories": Category.objects.all(),
            "keyword": keyword,
            "selected_category": category_id,
        }
    )


@staff_required
def add_product(request):

    form = StaffProductForm(
        request.POST or None,
        request.FILES or None
    )

    if form.is_valid():

        form.save()

        messages.success(
            request,
            "Thêm sản phẩm thành công."
        )

        return redirect(
            "staff_product_list"
        )

    return render(
        request,
        "staff/add_product.html",
        {
            "form": form
        }
    )


@staff_required
def edit_product(request, pk):

    product = get_object_or_404(
        Product,
        pk=pk
    )

    form = StaffProductForm(
        request.POST or None,
        request.FILES or None,
        instance=product
    )

    if form.is_valid():

        form.save()

        messages.success(
            request,
            "Cập nhật sản phẩm thành công."
        )

        return redirect(
            "staff_product_list"
        )

    return render(
        request,
        "staff/edit_product.html",
        {
            "form": form,
            "product": product
        }
    )


@staff_required
def delete_product(request, pk):

    product = get_object_or_404(
        Product,
        pk=pk
    )

    if request.method == "POST":

        product.delete()

        messages.success(
            request,
            "Xóa sản phẩm thành công."
        )

        return redirect(
            "staff_product_list"
        )

    return render(
        request,
        "staff/delete_product.html",
        {
            "product": product
        }
    )


# ==========================
# Orders
# ==========================

@staff_required
def order_list(request):

    orders = Order.objects.select_related(
        "user"
    ).order_by("-created_at")

    return render(
        request,
        "staff/order_list.html",
        {
            "orders": orders
        }
    )


@staff_required
def order_detail(request, pk):

    order = get_object_or_404(
        Order.objects.prefetch_related(
            "items__product"
        ),
        pk=pk
    )

    return render(
        request,
        "staff/order_detail.html",
        {
            "order": order,
            "items": order.items.all()
        }
    )


@staff_required
def update_order(request, pk):

    order = get_object_or_404(
        Order,
        pk=pk
    )

    if request.method == "POST":

        status = request.POST.get("status")

        if status:

            order.status = status

            order.save()

            messages.success(
                request,
                "Cập nhật trạng thái đơn hàng thành công."
            )

            return redirect(
                "staff_order_detail",
                pk=order.pk
            )

    return render(
        request,
        "staff/update_order.html",
        {
            "order": order,
            "choices": Order.STATUS_CHOICES,
        }
    )


# ==========================
# Profile
# ==========================

@staff_required
def profile(request):

    return render(
        request,
        "staff/profile.html"
    )


@staff_required
def change_password(request):

    form = PasswordChangeForm(
        request.user,
        request.POST or None
    )

    if form.is_valid():

        user = form.save()

        update_session_auth_hash(
            request,
            user
        )

        messages.success(
            request,
            "Đổi mật khẩu thành công."
        )

        return redirect(
            "staff_dashboard"
        )

    return render(
        request,
        "staff/change_password.html",
        {
            "form": form
        }
    )